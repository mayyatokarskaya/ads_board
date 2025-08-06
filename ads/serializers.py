from rest_framework import serializers

from ads.models import Ad, Comment


class AdSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = Ad
        fields = (
            "id",
            "title",
            "description",
            "price",
            "author",
            "author_email",
            "image",
            "created_at",
        )
        read_only_fields = ("id", "author_email", "created_at", "author")


class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "ad", "author", "author_email", "content", "created_at")
        read_only_fields = ("id", "author", "author_email", "created_at")
