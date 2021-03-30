from rest_framework_simplejwt.views import TokenViewBase

from dateflix_api.serializers import TokenObtainPairSerializer


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = TokenObtainPairSerializer
