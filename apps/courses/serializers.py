from rest_framework import serializers

from apps.users.serializers import UserSerializer

from . import models


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = models.Category
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""

    students = UserSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = models.Course
        fields = (
            "name",
            "description",
            "image",
            "price",
            "students",
            "category",
        )
