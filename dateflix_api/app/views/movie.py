from rest_framework import viewsets

from dateflix_api.app.models import Movie
from dateflix_api.app.serializers import MovieSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows movies to be viewed.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
