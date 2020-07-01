from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):

    text = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=True)
    is_updated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated']
