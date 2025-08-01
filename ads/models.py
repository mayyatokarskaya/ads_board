from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ad(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads")
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
