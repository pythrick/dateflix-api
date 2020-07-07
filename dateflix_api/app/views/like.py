from rest_framework import mixins, viewsets

from dateflix_api.app.models import Like
from dateflix_api.app.serializers import LikeSerializer


class LikeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows movies to be liked or disliked.
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
