import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    User = get_user_model()
    user = User.objects.create_user(
        email="testuser@example.com", password="testpassword"
    )
    return user


@pytest.mark.django_db
def test_retrieve_user_profile(api_client, create_user):
    url = reverse("users:profile")
    api_client.force_authenticate(user=create_user)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == create_user.email
    assert "first_name" in response.data
    assert "last_name" in response.data


@pytest.mark.django_db
def test_update_user_profile(api_client, create_user):
    url = reverse("users:profile")
    api_client.force_authenticate(user=create_user)

    data = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "password": "newpassword",
    }
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    create_user.refresh_from_db()
    assert create_user.first_name == "NewFirstName"
    assert create_user.last_name == "NewLastName"
    assert create_user.check_password("newpassword")


@pytest.mark.django_db
def test_update_user_profile_invalid_data(api_client, create_user):
    url = reverse("users:profile")
    api_client.force_authenticate(user=create_user)
    data = {"email": "not-an-email"}
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
