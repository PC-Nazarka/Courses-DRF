from rest_framework import generics, response, status

from apps.core.views import BaseViewSet, SimpleBaseViewSet
from apps.users.models import User

from . import models, permissions, serializers


class CourseViewSet(BaseViewSet):
    """ViewSet for Course model."""

    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(owner=self.request.user)


class AddStudentsToCourseView(generics.GenericAPIView):
    """View for add student to course."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=request.user.pk)
        if user in course.students.all():
            course.students.remove(user)
        else:
            course.students.add(user)
        return response.Response(status=status.HTTP_200_OK)


class TopicViewSet(SimpleBaseViewSet):
    """ViewSet for Topic model."""

    serializer_class = serializers.TopicSerializer
    queryset = models.Topic.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)


class TaskViewSet(SimpleBaseViewSet):
    """ViewSet for Task model."""

    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)


class AnswerViewSet(SimpleBaseViewSet):
    """ViewSet for Answer model."""

    serializer_class = serializers.AnswerSerializer
    queryset = models.Answer.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)


class CommentViewSet(SimpleBaseViewSet):
    """ViewSet for Comment model."""

    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(user=self.request.user)


class ReviewViewSet(SimpleBaseViewSet):
    """ViewSet for Review model."""

    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(user=self.request.user)


class CategoryListAPIView(generics.ListAPIView):
    """APIView for get list instanses of Category model."""

    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class CategoryAPIView(generics.RetrieveAPIView):
    """APIView for get instanse of Category model."""

    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
