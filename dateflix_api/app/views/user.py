from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from dateflix_api.app.models import User
from dateflix_api.app.serializers import TokenObtainPairSerializer, UserSerializer
from dateflix_api.app.services import instagram


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = instagram.authenticate(serializer.validated_data.pop("code"))
        serializer.validated_data.update({"instagram_user_id": response.get("user_id")})

        User = get_user_model()

        if User.objects.filter(instagram_user_id=response.get("user_id")).exists():
            raise PermissionDenied(detail=_("User already registered."))

        user = User.objects.create(**serializer.validated_data)
        refresh = TokenObtainPairSerializer.get_token(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)
