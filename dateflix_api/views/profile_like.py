from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from dateflix_api.models import ProfileLike
from dateflix_api.serializers import ProfileLikeSerializer


class ProfileLikeViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows movies to be liked or disliked.
    """

    queryset = ProfileLike.objects.all()
    serializer_class = ProfileLikeSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_like = serializer.save()
        match = bool(profile_like.match)
        profile_name = (
            profile_like.to_user.full_name if match else profile_like.to_user.short_name
        )
        profile_instagram = profile_like.to_user.instagram if match else ""
        response = {
            "movie": {
                "id": profile_like.movie.id,
                "title": profile_like.movie.title,
                "url": profile_like.movie.netflix_url,
                "image": profile_like.movie.image,
            },
            "profile": {
                "id": profile_like.to_user.id,
                "name": profile_name,
                "instagram": profile_instagram,
            },
            "match": match,
        }
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
