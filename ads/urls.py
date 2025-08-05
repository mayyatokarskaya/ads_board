from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ads.views import AdViewSet

from ads.views import CommentViewSet

router = DefaultRouter()
router.register(r"", AdViewSet)

router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
