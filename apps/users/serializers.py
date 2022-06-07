from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for representation `User`."""

    class Meta:
        model = get_user_model()
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
