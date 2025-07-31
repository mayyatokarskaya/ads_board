from rest_framework import serializers
from ads.models import Ad


class AdSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Ad
        fields = ("id", "title", "description", "price", "author", "author_email", "created_at")
        read_only_fields = ("id", "author_email", "created_at", "author")
