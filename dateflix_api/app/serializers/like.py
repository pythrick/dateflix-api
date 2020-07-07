from rest_framework import serializers

from dateflix_api.app.models import Like, Movie


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    movie = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Movie.objects.all()
    )

    class Meta:
        model = Like
        fields = ["id", "movie", "like", "user"]
