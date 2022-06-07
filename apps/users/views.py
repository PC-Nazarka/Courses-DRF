from django.contrib.auth import get_user_model
from rest_framework import viewsets

from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""

    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        """Get serializer class in dependencies of action."""
        return (
            serializers.UserReadSerializer
            if self.action in ("list", "retrieve")
            else serializers.UserWriteSerializer
        )
