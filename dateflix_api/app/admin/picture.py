from django.contrib import admin

from dateflix_api.app.models import Picture


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass
