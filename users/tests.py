import pytest
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()


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
