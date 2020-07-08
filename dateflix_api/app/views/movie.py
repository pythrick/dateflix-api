from rest_framework import viewsets

from dateflix_api.app.models import Movie
from dateflix_api.app.serializers import MovieSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows movies to be viewed.
    """

    serializer_class = MovieSerializer

    def get_queryset(self):
        movies_ids = [
            item["movie_id"] for item in self.request.user.likes.values("movie_id")
        ]
        return Movie.objects.exclude(id__in=movies_ids).all()
