from rest_framework import mixins, viewsets

from dateflix_api.models import Like
from dateflix_api.serializers import LikeSerializer


class LikeViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows movies to be liked or disliked.
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
