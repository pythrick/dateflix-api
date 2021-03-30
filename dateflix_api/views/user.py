from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from dateflix_api import settings
from dateflix_api.models import Picture, User
from dateflix_api.serializers import TokenObtainPairSerializer, UserSerializer
from dateflix_api.services import instagram


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = instagram.authenticate(
            serializer.validated_data.pop("code"),
            redirect_uri=settings.SIGNUP_REDIRECT_URI,  # noqa
        )
        user_id = response.get("user_id")
        access_token = response.get("access_token")
        profile = instagram.get_profile(access_token)
        username = profile.get("username")

        serializer.validated_data.update(
            {
                "instagram_user_id": user_id,
                "instagram": f"https://instagram.com/{username}",
            }
        )

        User = get_user_model()
        if User.objects.filter(instagram_user_id=response.get("user_id")).exists():
            raise PermissionDenied(detail=_("User already registered."))

        user = User.objects.create(**serializer.validated_data)

        # Get pictures URLs and store them in the Database
        images_ids = [d["id"] for d in profile["media"]["data"]]
        pictures = instagram.get_pictures(access_token, images_ids)
        for picture in pictures:
            Picture.objects.create(url=picture, user=user)

        refresh = TokenObtainPairSerializer.get_token(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)
