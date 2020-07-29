from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from dateflix_api.app.services import instagram


class TokenObtainPairSerializer(serializers.Serializer):

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["code"] = serializers.CharField()

    def validate(self, attrs):
        try:
            data = instagram.authenticate(attrs["code"])
        except Exception as e:
            raise exceptions.AuthenticationFailed(_("Invalid Instagram code."),) from e
        user_id = data.get("user_id")
        User = get_user_model()
        self.user = User.objects.filter(instagram_user_id=user_id).first()

        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"], "no_active_account",
            )

        refresh = self.get_token(self.user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return data

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)
