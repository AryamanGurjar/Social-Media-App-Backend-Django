from __future__ import annotations

from uuid import uuid4

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]
