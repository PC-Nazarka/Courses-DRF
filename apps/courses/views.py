from rest_framework import generics, status, views, viewsets
from rest_framework.response import Response

from apps.users.models import User

from . import models, serializers


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course model."""

    queryset = models.Course.objects.all()

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        """Get serializer class in dependencies of action."""
        return (
            serializers.CourseReadSerializer
            if self.action in ("list", "retrieve")
            else serializers.CourseWriteSerializer
        )


class AddStudentsToCourseView(views.APIView):
    """View for add student to course."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=request.user.pk)
        if user in course.students.all():
            course.students.remove(user)
        else:
            course.students.add(user)
        return Response(status=status.HTTP_200_OK)


class TopicViewSet(viewsets.ModelViewSet):
    """ViewSet for Topic model."""

    queryset = models.Topic.objects.all()

    def get_serializer_class(self):
        """Get serializer class in dependencies of action."""
        return (
            serializers.TopicReadSerializer
            if self.action in ("list", "retrieve")
            else serializers.TopicWriteSerializer
        )


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for Task model."""

    queryset = models.Task.objects.all()

    def get_serializer_class(self):
        """Get serializer class in dependencies of action."""
        return (
            serializers.TaskReadSerializer
            if self.action in ("list", "retrieve")
            else serializers.TaskWriteSerializer
        )


class AnswerViewSet(viewsets.ModelViewSet):
    """ViewSet for Answer model."""

    serializer_class = serializers.AnswerSerializer
    queryset = models.Answer.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model."""

    queryset = models.Comment.objects.all()

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Get serializer class in dependencies of action."""
        return (
            serializers.CommentReadSerializer
            if self.action in ("list", "retrieve")
            else serializers.CommentWriteSerializer
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review model."""

    queryset = models.Review.objects.all()

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Get serializer class in dependencies of action."""
        return (
            serializers.ReviewReadSeriaizer
            if self.action in ("list", "retrieve")
            else serializers.ReviewWriteSeriaizer
        )


class CategoryListAPIView(generics.ListAPIView):
    """APIView for get list instanses of Category model."""

    serializer_class = serializers.CategoryReadSerializer
    queryset = models.Category.objects.all()


class CategoryAPIView(generics.RetrieveAPIView):
    """APIView for get instanse of Category model."""

    serializer_class = serializers.CategoryReadSerializer
    queryset = models.Category.objects.all()
