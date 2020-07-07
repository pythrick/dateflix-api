from uuid import uuid4

from django.db import models


class ModelMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
