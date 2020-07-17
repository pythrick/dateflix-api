from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixin import ModelMixin


class Movie(ModelMixin):
    title = models.CharField(_("title"), max_length=250)
    url = models.URLField(_("url"))
    image = models.URLField(_("image"))
    netflix_id = models.IntegerField(_("Netflix Movie ID"))
    description = models.TextField(_("description"), blank=True, null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
