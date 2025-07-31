from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/token/", include("users.jwt_urls")),
    path("api/ads/", include("ads.urls")),
    # path("api/users/", include("users.urls")),  # пока заглушка
    path("api/auth/", include("rest_framework.urls")),
]