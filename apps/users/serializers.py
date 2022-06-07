from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserWriteSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = "__all__"


class UserReadSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "description",
        )
