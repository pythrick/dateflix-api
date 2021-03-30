from django.contrib import admin

from dateflix_api.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass
