from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixin import ModelMixin


class Match(ModelMixin):
    class Meta:
        unique_together = ("movie", "user", "user_match")

    movie = models.ForeignKey(
        "Movie", models.PROTECT, related_name="matchs", blank=False, null=False
    )
    user = models.ForeignKey(
        "User", models.PROTECT, related_name="matchs", blank=False, null=False
    )
    user_match = models.ForeignKey("User", models.PROTECT, blank=False, null=False)
