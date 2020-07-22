from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixin import ModelMixin


class Movie(ModelMixin):
    title = models.CharField(_("title"), max_length=250)
    netflix_url = models.URLField(_("url"))
    image = models.URLField(_("image"))
    justwatch_id = models.IntegerField(_("JustWatch ID"))
    tmdb_id = models.IntegerField(_("TMDB ID"))
    netflix_id = models.IntegerField(_("Netflix ID"))
    imdb_score = models.DecimalField(
        _("IMDB Score"), max_digits=3, decimal_places=1, null=True, blank=True
    )
    tmdb_score = models.DecimalField(
        _("TMDB Score"), max_digits=3, decimal_places=1, null=True, blank=True
    )
    description = models.TextField(_("description"), blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
