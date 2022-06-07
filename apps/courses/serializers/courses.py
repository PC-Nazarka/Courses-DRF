from rest_framework import serializers

from .. import models


class CategoryReadSerializer(serializers.ModelSerializer):
    """Serializer for read Category model."""

    courses = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
    )

    class Meta:
        model = models.Category
        fields = (
            "id",
            "name",
            "courses",
        )


class CourseWriteSerializer(serializers.ModelSerializer):
    """Serializer for write Course model."""

    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
    )

    class Meta:
        model = models.Course
        fields = (
            "id",
            "name",
            "description",
            "image",
            "price",
            "category",
        )


class CourseReadSerializer(serializers.ModelSerializer):
    """Serializer for read Course model."""

    students = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    category = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    topics = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
    )
    reviews = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
    )

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
            "topics",
            "reviews",
        )


class TopicWriteSerializer(serializers.ModelSerializer):
    """Serializer for write Topic model."""

    course = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = models.Topic
        fields = (
            "id",
            "title",
            "number",
            "course",
        )


class TopicReadSerializer(serializers.ModelSerializer):
    """Serializer for read Topic model."""

    course = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    tasks = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
    )

    class Meta:
        model = models.Topic
        fields = (
            "id",
            "title",
            "number",
            "course",
            "tasks",
        )


class TaskWriteSerializer(serializers.ModelSerializer):
    """Serializer for write Task model."""

    topic = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = models.Task
        fields = (
            "id",
            "type_task",
            "title",
            "text",
            "topic",
        )


class TaskReadSerializer(serializers.ModelSerializer):
    """Serializer for read Task model."""

    topic = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    answers = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
    )
    comments = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
    )

    class Meta:
        model = models.Task
        fields = (
            "id",
            "type_task",
            "title",
            "text",
            "topic",
            "answers",
            "comments",
        )


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for read and write Answer model."""

    task = serializers.PrimaryKeyRelatedField(
        queryset=models.Task.objects.all(),
    )

    class Meta:
        model = models.Answer
        fields = (
            "id",
            "is_true",
            "content",
            "task",
        )


class CommentWriteSerializer(serializers.ModelSerializer):
    """Serializer for write Comment model."""

    task = serializers.PrimaryKeyRelatedField(
        queryset=models.Task.objects.all(),
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=models.Comment.objects.all(),
    )

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "content",
            "task",
            "parent",
        )


class CommentReadSerializer(serializers.ModelSerializer):
    """Serializer for read Comment model."""

    task = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    parent = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "content",
            "task",
            "parent",
            "user",
        )
