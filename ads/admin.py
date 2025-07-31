from django.contrib import admin
from .models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "created_at")
    search_fields = ("title", "description", "author__email")
    list_filter = ("created_at", "price")
    ordering = ("-created_at",)
