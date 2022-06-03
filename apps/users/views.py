from django.contrib.auth import get_user_model
from rest_framework import viewsets

from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""

    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()
