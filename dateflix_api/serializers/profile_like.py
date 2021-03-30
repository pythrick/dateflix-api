from rest_framework import serializers

from dateflix_api.models import Movie, ProfileLike, User


class ProfileLikeSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    movie = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Movie.objects.all()
    )
    to_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )  # TODO: Validate if user has liked the movie

    class Meta:
        model = ProfileLike
        fields = ["id", "movie", "like", "to_user", "from_user"]
