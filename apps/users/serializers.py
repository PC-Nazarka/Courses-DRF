from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        exclude = (
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
            "date_joined",
            "is_superuser",
        )
