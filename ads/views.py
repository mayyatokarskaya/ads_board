from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ads.models import Ad
from ads.permissions import IsOwnerOrReadOnly
from ads.serializers import AdSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdListView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ads"] = Ad.objects.all()
        return context
