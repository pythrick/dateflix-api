from rest_framework import mixins, response, viewsets

from dateflix_api.app.models import User
from dateflix_api.app.serializers import ProfileSerializer


class MeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows current profile to be viewed.
    """

    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        # assumes the user is authenticated, handle this according your needs
        return response.Response(self.serializer_class(request.user).data)
