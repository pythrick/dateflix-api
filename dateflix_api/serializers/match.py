from rest_framework import serializers

from dateflix_api.models import Movie, ProfileLike, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "instagram"]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "url", "image"]


class MatchSerializer(serializers.ModelSerializer):
    from_user = ProfileSerializer()
    movie = MovieSerializer()

    class Meta:
        model = ProfileLike
        fields = ["from_user", "movie"]
