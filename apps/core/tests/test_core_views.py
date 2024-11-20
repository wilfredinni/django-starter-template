from django.urls import reverse
from django.test import Client


def test_ping_view():
    client = Client()
    response = client.get(reverse("ping"))
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_ping_view_method_not_allowed():
    client = Client()
    response = client.post(reverse("ping"))
    assert response.status_code == 405
    assert response.json() == {"detail": 'Method "POST" not allowed.'}
