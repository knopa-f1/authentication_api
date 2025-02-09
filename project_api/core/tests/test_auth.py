import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse("register")
    data = {"email": "newuser@example.com", "password": "securepassword"}

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert "email" in response.data


@pytest.mark.django_db
def test_login_user(api_client, test_user):
    url = reverse("login")
    data = {"email": "test@example.com", "password": "password123"}

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.data
    assert "refresh_token" in response.data


@pytest.mark.django_db
def test_refresh_token(api_client, test_user):
    login_url = reverse("login")
    refresh_url = reverse("refresh")

    login_response = api_client.post(login_url, {"email": "test@example.com", "password": "password123"})
    refresh_token = login_response.data["refresh_token"]

    # refresh token
    response = api_client.post(refresh_url, {"refresh_token": refresh_token})

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.data


@pytest.mark.django_db
def test_logout(api_client, test_user):
    login_url = reverse("login")
    logout_url = reverse("logout")

    login_response = api_client.post(login_url, {"email": "test@example.com", "password": "password123"})
    refresh_token = login_response.data["refresh_token"]

    response = api_client.post(logout_url, {"refresh_token": refresh_token})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] == "User logged out."


@pytest.mark.django_db
def test_get_user_data(api_client, test_user):
    url = reverse("me")

    login_url = reverse("login")
    login_response = api_client.post(login_url, {"email": "test@example.com", "password": "password123"})
    access_token = login_response.data["access_token"]

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == test_user.email


@pytest.mark.django_db
def test_update_user_info(api_client, test_user):
    url = reverse("me")

    login_url = reverse("login")
    login_response = api_client.post(login_url, {"email": "test@example.com", "password": "password123"})
    access_token = login_response.data["access_token"]

    data = {"username": "John Smith"}

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = api_client.put(url, data, format="json")

    assert response.status_code == 200
    assert response.data["username"] == "John Smith"
    assert response.data["email"] == "test@example.com"
