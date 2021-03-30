from django.db.models import F, OuterRef, Subquery
from rest_framework import viewsets

from dateflix_api.models import ProfileLike
from dateflix_api.serializers import MatchSerializer


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows playlist for movies to be viewed.
    """

    serializer_class = MatchSerializer

    def get_queryset(self):
        sub_query = (
            ProfileLike.objects.filter(
                movie=OuterRef("movie"), from_user=self.request.user, like=True
            )
            .annotate(match_user=F("to_user"))
            .values("to_user")
        )

        return ProfileLike.objects.filter(
            from_user__in=Subquery(sub_query),
            to_user=self.request.user,
            like=True,
        ).all()
