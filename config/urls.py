from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from users import jwt_urls
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from ads.views import AdListView

urlpatterns = [
    path("", AdListView.as_view(), name="home"),
    path("api/users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("api/token/", include(jwt_urls)),
    path("api/ads/", include("ads.urls")),
    path("api/auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
