from rest_framework import generics

from users.serializers import RegisterSerializer
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .serializers import PasswordResetSerializer, PasswordResetConfirmSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

User = get_user_model()


@extend_schema(tags=["Auth"])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data["email"])
        refresh = RefreshToken.for_user(user)
        reset_token = str(refresh.access_token)

        reset_link = f"http://localhost:8000/api/users/password-reset-confirm/?token={reset_token}"

        send_mail(
            "Сброс пароля",
            f"Используйте этот токен для сброса пароля: {reset_token}\nИли перейдите по ссылке: {reset_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response(
            {"status": "Письмо отправлено", "token": reset_token}
        )  # Токен для теста


@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Декодируем JWT-токен
        from rest_framework_simplejwt.tokens import AccessToken

        try:
            token = AccessToken(serializer.validated_data["token"])
            user_id = token["user_id"]
            user = User.objects.get(id=user_id)
        except:
            return Response({"error": "Неверный токен"}, status=400)

        # Устанавливаем новый пароль
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"status": "Пароль изменен"})
