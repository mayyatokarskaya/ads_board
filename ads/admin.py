from django.contrib import admin

from .models import Ad, Comment


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "created_at")
    search_fields = ("title", "description", "author__email")
    list_filter = ("created_at", "price")
    ordering = ("-created_at",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "author", "ad", "created_at")
    list_filter = ("created_at", "ad")
    search_fields = ("content", "author__email")