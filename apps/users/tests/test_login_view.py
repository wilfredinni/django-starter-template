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
    assert "expiry" in response.data
    assert "token" in response.data
    assert "user" in response.data
    assert "email" in response.data["user"]
    assert "first_name" in response.data["user"]
    assert "last_name" in response.data["user"]
    assert response.data["expiry"] is not None
    assert response.data["token"] is not None
    assert response.data["user"] is not None
    assert response.data["user"]["email"] == "testuser@test.com"


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


@pytest.mark.django_db
def test_login_get_not_allowed(api_client):
    url = reverse("users:knox_login")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_login_put_not_allowed(api_client):
    url = reverse("users:knox_login")
    data = {"email": "testuser@test.com", "password": "testpassword"}
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_login_patch_not_allowed(api_client):
    url = reverse("users:knox_login")
    data = {"email": "testuser@test.com", "password": "testpassword"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_login_delete_not_allowed(api_client):
    url = reverse("users:knox_login")
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
