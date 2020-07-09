from rest_framework import serializers

from dateflix_api.app.models import Picture, User


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ["url"]


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="short_name", read_only=True)
    pictures = PictureSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "name", "bio", "pictures"]
