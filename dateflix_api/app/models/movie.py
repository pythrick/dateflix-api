from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixin import ModelMixin


class Movie(ModelMixin):
    title = models.CharField(_("title"), max_length=250)
    url = models.URLField(_("url"))
    image = models.URLField(_("image"))
    description = models.TextField(_("description"))
