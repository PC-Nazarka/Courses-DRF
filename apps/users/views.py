from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for Use model."""

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
