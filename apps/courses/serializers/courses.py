from rest_framework import serializers

from .. import models


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for representing `Category`."""

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


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for representing `Course`."""

    students = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
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
            "created",
        )


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for representing `Topic`."""

    course = serializers.PrimaryKeyRelatedField(
        queryset=models.Course.objects.all(),
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


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for representing `Task`."""

    topic = serializers.PrimaryKeyRelatedField(
        queryset=models.Topic.objects.all(),
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
    """Serializer for representing `Answer`."""

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


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for representing `Comment`."""

    task = serializers.PrimaryKeyRelatedField(
        queryset=models.Task.objects.all(),
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=models.Comment.objects.all(),
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
