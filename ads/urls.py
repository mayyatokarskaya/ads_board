from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ads.views import AdViewSet

router = DefaultRouter()
router.register(r"", AdViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
