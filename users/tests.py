import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from users.serializers import UserSerializer
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()


# фикстуры
@pytest.fixture
def user():
    return User.objects.create_user(
        email="testuser@example.com", password="testpass123"
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
def test_create_user():
    user = User.objects.create_user(email="test@example.com", password="password123")
    assert user.email == "test@example.com"
    assert user.check_password("password123")
    assert not user.is_staff
    assert user.is_active


@pytest.mark.django_db
def test_create_superuser():
    admin = User.objects.create_superuser(
        email="admin@example.com", password="adminpass"
    )
    assert admin.is_staff
    assert admin.is_superuser
    assert admin.email == "admin@example.com"
    assert admin.check_password("adminpass")


@pytest.mark.django_db
def test_user_str_method():
    user = User.objects.create_user(email="strtest@example.com", password="pass")
    assert str(user) == "strtest@example.com"


@pytest.mark.django_db
def test_user_serializer():
    user = User.objects.create_user(
        email="serialize@example.com", full_name="Test User", password="pass"
    )
    serializer = UserSerializer(user)
    data = serializer.data
    assert data["email"] == "serialize@example.com"
    assert data["full_name"] == "Test User"
    assert "date_joined" in data
    assert "id" in data


@pytest.mark.django_db
def test_jwt_authentication():
    client = APIClient()
    user = User.objects.create_user(email="jwtuser@example.com", password="jwtpass123")

    url = reverse("token_obtain_pair")
    response = client.post(
        url, {"email": "jwtuser@example.com", "password": "jwtpass123"}, format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_create_user_without_email_raises():
    User = get_user_model()
    with pytest.raises(ValueError):
        User.objects.create_user(email=None, password="testpass")


@pytest.mark.django_db
def test_register_api():
    client = APIClient()
    url = reverse("register")
    data = {
        "email": "new@example.com",
        "full_name": "New User",
        "password": "newpass123",
        "password2": "newpass123",
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="new@example.com").exists()


# Тест сброса пароля
@pytest.mark.django_db
def test_password_reset_flow(user, api_client):
    # 1. Запрос сброса пароля
    reset_url = reverse("api_password_reset")
    response = api_client.post(reset_url, {"email": user.email})
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data  # Проверяем, что токен возвращается

    # 2. Подтверждение сброса пароля
    token = response.data["token"]  # Используем реальный токен из ответа
    confirm_url = reverse("api_password_reset_confirm")
    response = api_client.post(
        confirm_url,
        {
            "token": token,
            "new_password": "newpassword123",
            "password2": "newpassword123",
        },
    )
    assert response.status_code == status.HTTP_200_OK

    # 3. Проверяем, что пароль действительно изменился
    user.refresh_from_db()
    assert user.check_password("newpassword123")
