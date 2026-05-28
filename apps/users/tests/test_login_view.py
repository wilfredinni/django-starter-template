from unittest.mock import patch

from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import CustomUser as User


class LoginViewTests(APITestCase):
    """Test suite for the JWT login view"""

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("v1:users:login")
        cls.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword123"
        )
        cls.valid_credentials = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }

    def test_login_success(self):
        """Test successful user login with JWT token response"""
        response = self.client.post(self.url, self.valid_credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify JWT response structure: access + refresh + user
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

        # Verify user data in response
        user_data = response.data["user"]
        self.assertEqual(user_data["email"], self.user.email)

        # Verify the access token is a valid JWT
        access_token = response.data["access"]
        self.assertIsInstance(access_token, str)
        self.assertTrue(access_token.count(".") == 2)  # JWT has 3 parts

    def test_login_success_authenticated_request(self):
        """JWT access token can authenticate subsequent requests"""
        response = self.client.post(self.url, self.valid_credentials, format="json")
        access_token = response.data["access"]

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        profile_url = reverse("v1:users:profile")
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        invalid_cases = [
            {"email": "wrong@example.com", "password": "wrongpassword"},
            {"email": self.user.email, "password": "wrongpassword"},
            {
                "email": "wrong@example.com",
                "password": self.valid_credentials["password"],
            },
        ]

        for invalid_data in invalid_cases:
            with self.subTest(data=invalid_data):
                response = self.client.post(self.url, invalid_data, format="json")
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                self.assertIn("detail", response.data)

    def test_login_inactive_user(self):
        """Test login attempt for inactive user"""
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, self.valid_credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_login_missing_fields(self):
        """Test login with missing required fields"""
        required_fields = ["email", "password"]

        for field in required_fields:
            with self.subTest(field=field):
                data = self.valid_credentials.copy()
                data.pop(field)
                response = self.client.post(self.url, data, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)

    def test_login_invalid_methods(self):
        """Test that only POST method is allowed"""
        methods = ["get", "put", "patch", "delete"]

        for method in methods:
            with self.subTest(method=method):
                response = getattr(self.client, method)(self.url)
                self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
                self.assertIn("POST", response["Allow"])

    def test_login_throttling(self):
        """Test that login attempts are rate limited"""
        from apps.users.throttles import UserLoginRateThrottle

        # Create a test throttle class with very low rate for testing
        class TestLoginThrottle(UserLoginRateThrottle):
            rate = "1/minute"
            cache = cache  # Use default cache instead of throttle cache

            def get_cache_key(self, request, view):
                # Use a consistent test key
                return "throttle_login_test_key"

        # Clear any existing throttle state
        cache.delete("throttle_login_test_key")

        # Patch the view's throttle classes
        with patch("apps.users.views.LoginView.throttle_classes", [TestLoginThrottle]):
            # First request should succeed
            response = self.client.post(self.url, self.valid_credentials, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Second request should be throttled
            response = self.client.post(self.url, self.valid_credentials, format="json")
            self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_login_response_headers(self):
        """Test login response headers and content type"""
        response = self.client.post(self.url, self.valid_credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertTrue(response["X-Frame-Options"] == "DENY")
        self.assertTrue(response["X-Content-Type-Options"] == "nosniff")

    def test_concurrent_login(self):
        """Test that multiple concurrent logins work correctly with JWT"""
        # Create multiple JWT tokens for same user
        access_tokens = []
        for _ in range(3):
            response = self.client.post(self.url, self.valid_credentials, format="json")
            access_tokens.append(response.data["access"])

        # All access tokens should be valid
        for access_token in access_tokens:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
            profile_url = reverse("v1:users:profile")
            response = self.client.get(profile_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
