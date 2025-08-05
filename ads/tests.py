import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ads.models import Ad
from users.models import User


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


@pytest.mark.django_db
def test_list_ads(auth_client, ad):
    url = reverse("ad-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data["results"]) >= 1


@pytest.mark.django_db
def test_retrieve_ad(auth_client, ad):
    url = reverse("ad-detail", args=[ad.id])
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == ad.title


@pytest.mark.django_db
def test_ad_serializer_author_email(auth_client, user, ad):
    url = reverse("ad-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert len(response.data["results"]) > 0
    assert "author_email" in response.data["results"][0]
    assert response.data["results"][0]["author_email"] == user.email


@pytest.mark.django_db
def test_retrieve_nonexistent_ad(auth_client):
    url = reverse("ad-detail", args=[999])
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# Новые тесты
@pytest.mark.django_db
def test_pagination(auth_client):
    user = User.objects.create_user(email="pagination@test.com", password="testpass")
    for i in range(15):
        Ad.objects.create(title=f"Ad {i}", price=100 + i, author=user)

    url = reverse("ad-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 15
    assert len(response.data["results"]) == 10


@pytest.mark.django_db
def test_ordering(auth_client):
    user = User.objects.create_user(email="order@test.com", password="testpass")
    ad1 = Ad.objects.create(title="Ad 1", price=100, author=user)
    ad2 = Ad.objects.create(title="Ad 2", price=200, author=user)

    url = reverse("ad-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == ad2.id