from rest_framework import viewsets
from django.db.models import OuterRef, Subquery

from dateflix_api.app.models import ProfileLike
from dateflix_api.app.serializers import MatchSerializer


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows playlist for movies to be viewed.
    """

    serializer_class = MatchSerializer

    def get_queryset(self):
        sub_query = ProfileLike.objects.filter(
            movie=OuterRef("movie"), from_user=self.request.user, like=True
        ).annotate(match_user=F("to_user"))

        match = ProfileLike.objects.filter(
            from_user__in=SubQuery(sub_query), to_user=self.request.user, like=True,
        )
        print(match)
        return match
        # movies_ids = [item["movie_id"] for item in self.request.user.chosen_likes.all()]
        # return ProfileLike.objects.filter(to_user=self.request.user).all()
