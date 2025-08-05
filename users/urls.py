from django.urls import path
from users.views import RegisterView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetView as AuthPasswordResetView
from django.contrib.auth.views import (
    PasswordResetConfirmView as AuthPasswordResetConfirmView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    # API endpoints  (кастомные вьюхи)
    path("api/password-reset/", PasswordResetView.as_view(), name="api_password_reset"),
    path(
        "api/password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="api_password_reset_confirm",
    ),
    # Стандартные вьюхи Django
    path("password-reset/", AuthPasswordResetView.as_view(), name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        AuthPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
