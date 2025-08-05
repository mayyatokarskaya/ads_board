from django.views.generic import TemplateView
from rest_framework import viewsets

from ads.models import Ad
from ads.permissions import IsAdminOrOwnerOrReadOnly
from ads.serializers import AdSerializer

from ads.models import Comment
from ads.serializers import CommentSerializer

from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


class AdPagination(PageNumberPagination):
    page_size = 10


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
    pagination_class = AdPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdListView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ads"] = Ad.objects.all()
        return context


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
