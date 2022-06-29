from apps.core.serializers import BaseSerializer, serializers

from .. import models


class ReviewSerializer(BaseSerializer):
    """Serializer for representing `Review`."""

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=models.Course.objects.all(),
    )

    def validate_course(self, data):
        """Check for single created review for course."""
        other_reviews = models.Review.objects.filter(course_id=data.id).filter(
            user_id=self._user.id
        )
        if other_reviews and self._request.method == "POST":
            raise serializers.ValidationError(
                "You can't create more one review for course",
            )
        return data

    def validate_rating(self, data):
        """Check for correct value of rating."""
        if data not in range(0, 6):
            raise serializers.ValidationError(
                "Rating must be in range from 0 to 5.",
            )
        return data

    class Meta:
        model = models.Review
        fields = (
            "id",
            "rating",
            "review",
            "user",
            "course",
            "created",
            "modified",
        )
