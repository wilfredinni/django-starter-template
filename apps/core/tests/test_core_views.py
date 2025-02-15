import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_ping_view(api_client):
    url = reverse("ping")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ping": "pong"}


@pytest.mark.django_db
def test_ping_view_method_not_allowed(api_client):
    url = reverse("ping")
    response = api_client.post(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == {"detail": 'Method "POST" not allowed.'}


@pytest.mark.django_db
def test_ping_view_put_not_allowed(api_client):
    url = reverse("ping")
    response = api_client.put(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_ping_view_patch_not_allowed(api_client):
    url = reverse("ping")
    response = api_client.patch(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_ping_view_delete_not_allowed(api_client):
    url = reverse("ping")
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
