from rest_framework.routers import DefaultRouter
from ads.views import AdViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"", AdViewSet)

urlpatterns = [
    path("", include(router.urls)),
]