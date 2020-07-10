from django.contrib import admin

from dateflix_api.app.models import ProfileLike


@admin.register(ProfileLike)
class ProfileLikeAdmin(admin.ModelAdmin):
    pass
