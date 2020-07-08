from rest_framework import viewsets

from dateflix_api.app.models import Movie
from dateflix_api.app.serializers import MovieSerializer


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows playlist for movies to be viewed.
    """

    serializer_class = MovieSerializer

    def get_queryset(self):
        movies_ids = [
            item["movie_id"]
            for item in self.request.user.likes.filter(like=True).values("movie_id")
        ]
        return Movie.objects.filter(id__in=movies_ids).all()
