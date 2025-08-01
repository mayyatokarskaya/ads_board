from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", include("users.jwt_urls")),
    path("api/ads/", include("ads.urls")),
    # path("api/users/", include("users.urls")),  # пока заглушка
    path("api/auth/", include("rest_framework.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
