from rest_framework import serializers

from .. import models


class ReviewSeriaizer(serializers.ModelSerializer):
    """Serializer for representing `Review`."""

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=models.Course.objects.all(),
    )

    class Meta:
        model = models.Review
        fields = (
            "id",
            "rating",
            "review",
            "user",
            "course",
        )
