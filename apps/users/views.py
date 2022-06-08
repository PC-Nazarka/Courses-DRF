from rest_framework import generics, response, status

from .serializers import RefreshTokenSerializer


class LogoutView(generics.GenericAPIView):
    """View for logout.

    JWT Token move to blacklist.
    """

    serializer_class = RefreshTokenSerializer

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return response.Response(
            {"message": "Пользователь вышел"},
            status=status.HTTP_204_NO_CONTENT,
        )
