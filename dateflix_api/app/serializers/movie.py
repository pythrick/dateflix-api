from rest_framework import serializers

from dateflix_api.app.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "netflix_url", "image", "description"]
