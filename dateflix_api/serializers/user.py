from rest_framework import serializers

from dateflix_api.models import User


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "bio",
            "birthday_date",
            "code",
        ]
