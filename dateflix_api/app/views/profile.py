from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from dateflix_api.app.models import Movie, User
from dateflix_api.app.serializers import ProfileSerializer


class ProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows profiles to be viewed.
    """

    serializer_class = ProfileSerializer

    def get_queryset(self):
        movie_id = self.request.query_params.get("movie_id", None)
        movie = get_object_or_404(Movie, pk=movie_id)
        return (
            User.objects.filter(likes__movie=movie)
            .exclude(pk=self.request.user.pk)
            .all()
        )
