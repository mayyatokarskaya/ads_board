import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ads.models import Ad
from ads.permissions import IsOwnerOrReadOnly, IsAdminOrOwnerOrReadOnly
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

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass"
    )

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


# Добавляем в существующий ads/tests.py

@pytest.mark.django_db
def test_is_owner_or_read_only_permission(api_client, auth_client, user, another_user, ad):
    permission = IsOwnerOrReadOnly()
    request = type('Request', (), {'method': 'GET', 'user': None})()  # Анонимный запрос

    # 1. Проверка SAFE_METHODS (GET, HEAD, OPTIONS)
    assert permission.has_object_permission(request, None, ad)  # Должен разрешить

    # 2. Проверка изменения для автора
    request.method = 'PUT'
    request.user = user  # Владелец объявления
    assert permission.has_object_permission(request, None, ad)

    # 3. Проверка изменения для другого пользователя
    request.user = another_user  # Не владелец
    assert not permission.has_object_permission(request, None, ad)


@pytest.mark.django_db
def test_is_admin_or_owner_or_read_only_permission(api_client, auth_client, user, another_user, admin_user, ad):
    permission = IsAdminOrOwnerOrReadOnly()
    request = type('Request', (), {'method': 'GET', 'user': None})()  # Анонимный запрос

    # 1. Проверка SAFE_METHODS
    assert permission.has_object_permission(request, None, ad)

    # 2. Проверка для администратора
    request.method = 'DELETE'
    request.user = admin_user  # Администратор
    assert permission.has_object_permission(request, None, ad)

    # 3. Проверка для владельца
    request.user = user  # Владелец
    assert permission.has_object_permission(request, None, ad)

    # 4. Проверка для другого пользователя
    request.user = another_user  # Не владелец и не админ
    assert not permission.has_object_permission(request, None, ad)