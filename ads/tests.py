import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ads.models import Ad
from users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return User.objects.create_user(
        email="testuser@example.com", password="testpass123"
    )


@pytest.fixture
def another_user():
    return User.objects.create_user(email="other@example.com", password="testpass123")


@pytest.fixture
def ad(user):
    return Ad.objects.create(
        title="Test Ad", description="Test description", price=100.00, author=user
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def another_auth_client(another_user):
    client = APIClient()
    client.force_authenticate(user=another_user)
    return client


def test_list_ads(api_client, ad):
    url = reverse("ad-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1


def test_retrieve_ad(api_client, ad):
    url = reverse("ad-detail", args=[ad.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == ad.title


def test_create_ad(auth_client, user):
    url = reverse("ad-list")
    data = {
        "title": "New Ad",
        "description": "Created via test",
        "price": 1234.56,
    }
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Ad.objects.filter(title="New Ad", author=user).exists()


def test_update_ad_owner(auth_client, ad):
    url = reverse("ad-detail", args=[ad.id])
    data = {"title": "Updated Title"}
    response = auth_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    ad.refresh_from_db()
    assert ad.title == "Updated Title"


def test_update_ad_forbidden(another_auth_client, ad):
    url = reverse("ad-detail", args=[ad.id])
    data = {"title": "Should Fail"}
    response = another_auth_client.patch(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_ad_owner(auth_client, ad):
    url = reverse("ad-detail", args=[ad.id])
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Ad.objects.filter(id=ad.id).exists()


def test_delete_ad_forbidden(another_auth_client, ad):
    url = reverse("ad-detail", args=[ad.id])
    response = another_auth_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Ad.objects.filter(id=ad.id).exists()


def test_create_ad_unauthenticated(api_client):
    url = reverse("ad-list")
    data = {
        "title": "Should Fail",
        "description": "No token",
        "price": 1000,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_ad_serializer_author_email(auth_client, user, ad):
    url = reverse("ad-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "author_email" in response.data[0]
    assert response.data[0]["author_email"] == user.email


def test_retrieve_nonexistent_ad(api_client):
    url = reverse("ad-detail", args=[999])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
