from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixin import ModelMixin


class Like(ModelMixin):
    class Meta:
        unique_together = ("movie", "user")

    like = models.BooleanField(_("like"), blank=False, null=False)
    movie = models.ForeignKey(
        "Movie", models.PROTECT, related_name="likes", blank=False, null=False
    )
    user = models.ForeignKey(
        "User", models.PROTECT, related_name="likes", blank=False, null=False
    )
