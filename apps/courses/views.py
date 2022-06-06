from rest_framework import status, views, viewsets
from rest_framework.response import Response

from apps.users.models import User

from . import models, serializers


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course model."""

    serializer_class = serializers.CourseCreateSerializer
    queryset = models.Course.objects.all()

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        """Get serializer class in dependencies of action."""
        return (
            serializers.CourseSerializer
            if self.action in ("list", "retrieve")
            else serializers.CourseCreateSerializer
        )


class AddStudentsToCourseView(views.APIView):
    """View for add student to course."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=request.user.pk)
        if user in course.students.all():
            course.students.remove(User.objects.get(pk=request.user.pk))
        else:
            course.students.add(User.objects.get(pk=request.user.pk))
        return Response(status=status.HTTP_200_OK)


class TopicViewSet(viewsets.ModelViewSet):
    """ViewSet for Topic model."""

    serializer_class = serializers.TopicSerializer
    queryset = models.Topic.objects.all()
