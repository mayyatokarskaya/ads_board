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
