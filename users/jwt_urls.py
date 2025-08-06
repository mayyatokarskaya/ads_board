from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(post=extend_schema(tags=["Auth"], summary="JWT вход (логин)"))
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema_view(post=extend_schema(tags=["Auth"], summary="JWT обновление токена"))
class CustomTokenRefreshView(TokenRefreshView):
    pass


urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
