from rest_framework import generics
from users.models import User
from users.serializers import RegisterSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Auth"])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
