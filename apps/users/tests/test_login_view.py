import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import CustomUser as User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    return User.objects.create_user(email="testuser@test.com", password="testpassword")


@pytest.mark.django_db
def test_login_success(api_client, create_user):
    url = reverse("users:knox_login")
    data = {"email": "testuser@test.com", "password": "testpassword"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data


@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    url = reverse("users:knox_login")
    data = {"email": "wronguser@test.com", "password": "wrongpassword"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_missing_fields(api_client):
    url = reverse("users:knox_login")
    data = {"email": "testuser@test.com"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST