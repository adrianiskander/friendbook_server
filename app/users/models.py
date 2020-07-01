from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    token = models.CharField(max_length=1024, default='')
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
