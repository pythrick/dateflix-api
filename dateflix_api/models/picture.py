from django.db import models

from .mixin import ModelMixin


class Picture(ModelMixin):
    url = models.URLField(blank=False, null=False, max_length=300)
    user = models.ForeignKey("User", models.CASCADE, related_name="pictures")
