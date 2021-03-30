from django.contrib import admin

from dateflix_api.models import Picture


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass
