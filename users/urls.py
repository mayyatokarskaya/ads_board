from django.urls import path
from users.views import RegisterView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
