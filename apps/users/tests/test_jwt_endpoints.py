from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import CustomUser as User


class TokenRefreshTests(APITestCase):
    """Test suite for JWT token refresh endpoint"""

    @classmethod
    def setUpTestData(cls):
        cls.login_url = reverse("v1:users:login")
        cls.refresh_url = reverse("v1:users:token_refresh")
        cls.profile_url = reverse("v1:users:profile")
        cls.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword123"
        )
        cls.credentials_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }

    def _get_tokens(self):
        """Helper to get a valid access/refresh token pair."""
        response = self.client.post(self.login_url, self.credentials_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["access"], response.data["refresh"]

    def test_token_refresh_success(self):
        """Test refreshing an access token with a valid refresh token."""
        _access, refresh = self._get_tokens()
        response = self.client.post(self.refresh_url, {"refresh": refresh}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

        # With ROTATE_REFRESH_TOKENS=True, a new refresh token is also issued
        self.assertIn("refresh", response.data)

        # The new access token should work
        new_access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {new_access}")
        profile_response = self.client.get(self.profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)

    def test_token_refresh_invalid(self):
        """Test refresh with invalid/expired token."""
        response = self.client.post(
            self.refresh_url, {"refresh": "invalid_token"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_missing_token(self):
        """Test refresh with missing token."""
        response = self.client.post(self.refresh_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("refresh", response.data)

    def test_token_refresh_blacklisted(self):
        """Test that a blacklisted refresh token is rejected."""
        _access, refresh = self._get_tokens()

        # Blacklist the refresh token (logout)
        logout_url = reverse("v1:users:logout")
        self.client.post(logout_url, {"refresh": refresh}, format="json")

        # Try to refresh with the blacklisted token
        response = self.client.post(self.refresh_url, {"refresh": refresh}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenVerifyTests(APITestCase):
    """Test suite for JWT token verify endpoint"""

    @classmethod
    def setUpTestData(cls):
        cls.login_url = reverse("v1:users:login")
        cls.verify_url = reverse("v1:users:token_verify")
        cls.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword123"
        )
        cls.credentials_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }

    def test_token_verify_valid(self):
        """Test verifying a valid access token."""
        response = self.client.post(self.login_url, self.credentials_data, format="json")
        access_token = response.data["access"]

        response = self.client.post(
            self.verify_url, {"token": access_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_verify_invalid(self):
        """Test verifying an invalid token."""
        response = self.client.post(
            self.verify_url, {"token": "invalid.token.here"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_verify_missing_token(self):
        """Test verify with missing token."""
        response = self.client.post(self.verify_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("token", response.data)


class LogoutTests(APITestCase):
    """Test suite for JWT logout (token blacklist) endpoint"""

    @classmethod
    def setUpTestData(cls):
        cls.login_url = reverse("v1:users:login")
        cls.logout_url = reverse("v1:users:logout")
        cls.refresh_url = reverse("v1:users:token_refresh")
        cls.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword123"
        )
        cls.credentials_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }

    def test_logout_success(self):
        """Test that a refresh token is blacklisted on logout."""
        response = self.client.post(self.login_url, self.credentials_data, format="json")
        refresh_token = response.data["refresh"]

        logout_response = self.client.post(
            self.logout_url, {"refresh": refresh_token}, format="json"
        )
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

    def test_logout_no_credentials_required(self):
        """Test that logout does not require authentication."""
        logout_response = self.client.post(
            self.logout_url, {"refresh": "some_token"}, format="json"
        )
        # Invalid tokens return 401 from SimpleJWT's TokenBlacklistView
        self.assertEqual(logout_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_missing_refresh(self):
        """Test logout with missing refresh token."""
        response = self.client.post(self.logout_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("refresh", response.data)
