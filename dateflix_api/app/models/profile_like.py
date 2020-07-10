from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixin import ModelMixin


class ProfileLike(ModelMixin):
    class Meta:
        unique_together = ("movie", "from_user", "to_user")

    like = models.BooleanField(_("like"), blank=False, null=False)
    movie = models.ForeignKey(
        "Movie", models.PROTECT, related_name="profile_likes", blank=False, null=False
    )
    from_user = models.ForeignKey(
        "User", models.PROTECT, related_name="chosen_likes", blank=False, null=False
    )
    to_user = models.ForeignKey(
        "User", models.PROTECT, related_name="received_likes", blank=False, null=False
    )

    @property
    def match(self) -> bool:
        if self.like:
            return ProfileLike.objects.filter(
                from_user=self.to_user, movie=self.movie, like=True
            ).exists()
        return False
