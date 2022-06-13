from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserSerializer(serializers.ModelSerializer):
    """Serializer for representation `User`."""

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "last_login",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "description",
            "courses_student",
            "pass_courses",
            "favorite_courses",
            "want_pass_courses",
            "archive_courses",
            "courses",
        )


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {"bad_token": _("Token is invalid or expired")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
