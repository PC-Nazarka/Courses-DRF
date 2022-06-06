from rest_framework import serializers

from .. import models


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = models.Category
        fields = (
            "id",
            "name",
        )


class CourseCreateSerializer(serializers.ModelSerializer):
    """Serializer for create Course model."""

    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
    )

    class Meta:
        model = models.Course
        fields = (
            "name",
            "description",
            "image",
            "price",
            "category",
        )


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for create Course model."""

    students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Course
        fields = (
            "id",
            "name",
            "description",
            "image",
            "price",
            "students",
            "category",
            "owner",
        )


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for Topic model."""

    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Topic
        fields = (
            "id",
            "title",
            "number",
            "course",
        )


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""

    topic = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Task
        fields = (
            "id",
            "type_task",
            "title",
            "text",
            "topic",
        )


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for Answer model."""

    task = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Answer
        fields = (
            "id",
            "is_true",
            "content",
            "task",
        )


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    task = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "content",
            "task",
            "parent",
            "user",
        )
