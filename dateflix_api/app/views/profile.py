from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from dateflix_api.app.models import Movie, ProfileLike, User
from dateflix_api.app.serializers import ProfileSerializer


class ProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows profiles to be viewed.
    """

    serializer_class = ProfileSerializer

    def get_queryset(self):
        movie_id = self.request.query_params.get("movie_id", None)
        movie = get_object_or_404(Movie, pk=movie_id)
        user = self.request.user
        users_ids = list(
            ProfileLike.objects.filter(movie=movie, from_user=user)
            .values_list("to_user_id", flat=True)
            .all()
        )
        users_ids.append(user.pk)
        return User.objects.filter(likes__movie=movie).exclude(pk__in=users_ids).all()
