import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_user_success(api_client):
    url = reverse("users:create")
    data = {
        "email": "newuser@example.com",
        "password": "newpassword",
        "password2": "newpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.filter(email="newuser@example.com").exists()


@pytest.mark.django_db
def test_create_user_missing_fields(api_client):
    url = reverse("users:create")
    data = {
        "email": "newuser@example.com"
        # Missing password and password2
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_user_invalid_data(api_client):
    url = reverse("users:create")
    data = {
        "email": "not-an-email",
        "password": "newpassword",
        "password2": "newpassword",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST