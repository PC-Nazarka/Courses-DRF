from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from apps.core.service import PaginationObject
from apps.users.models import User

from . import models, serializers


class BaseViewSet(viewsets.ModelViewSet):
    """Base ViewSet for other views."""

    pagination_class = PaginationObject


class CourseViewSet(BaseViewSet):
    """ViewSet for Course model."""

    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.all()

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
        return Response(status=status.HTTP_200_OK)


class TopicViewSet(BaseViewSet):
    """ViewSet for Topic model."""

    serializer_class = serializers.TopicSerializer
    queryset = models.Topic.objects.all()


class TaskViewSet(BaseViewSet):
    """ViewSet for Task model."""

    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()


class AnswerViewSet(BaseViewSet):
    """ViewSet for Answer model."""

    serializer_class = serializers.AnswerSerializer
    queryset = models.Answer.objects.all()


class CommentViewSet(BaseViewSet):
    """ViewSet for Comment model."""

    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(user=self.request.user)


class ReviewViewSet(BaseViewSet):
    """ViewSet for Review model."""

    serializer_class = serializers.ReviewSeriaizer
    queryset = models.Review.objects.all()

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
