from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions as permis
from rest_framework import response, status
from rest_framework.views import APIView

from apps.core import views
from apps.users.models import User

from . import models, permissions, serializers


class CourseViewSet(views.BaseViewSet):
    """ViewSet for Course model."""

    serializer_class = serializers.CourseSerializer
    queryset = models.Course.objects.filter(status=models.Course.Status.READY)
    permission_classes = (permissions.IsCreatorOrStudent,)

    def get_object(self) -> models.Course:
        """Overriden for get object, because some object hasn't status `READY`."""
        return models.Course.objects.get(pk=self.kwargs["pk"])

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(owner=self.request.user)

    def search_queryset(self, object_list):
        """Filter queryset by search query."""
        query_search = self.request.GET.get("search")
        if query_search:
            return object_list.filter(
                Q(name__icontains=query_search)
                | Q(description__icontains=query_search),
            )
        return object_list

    def category_queryset(self, object_list):
        """Filter queryset by cateofry query."""
        query_category = self.request.GET.get("category")
        if query_category:
            return object_list.filter(
                category=query_category,
            )
        return object_list

    def get_queryset(self):
        """Get search result."""
        object_list = self.queryset
        object_list = self.search_queryset(object_list)
        object_list = self.category_queryset(object_list)
        return object_list


class AddStudentsToCourseView(APIView):
    """View for add student to course."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=request.user.pk)
        message = ""
        if user in course.students.all():
            course.students.remove(user)
            message = "remove"
            if user in course.want_pass_users.all():
                course.want_pass_users.remove(user)
            if user in course.archive_users.all():
                course.archive_users.remove(user)
        else:
            course.students.add(user)
            message = "add"
        return response.Response(
            data={"message": f"Success {message} students to course"},
            status=status.HTTP_200_OK,
        )


class AddCourseToInterestView(APIView):
    """View for course to interest by some user."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=self.request.user.pk)
        message = ""
        if user in course.interest_users.all():
            course.interest_users.remove(user)
            message = "remove"
        else:
            course.interest_users.add(user)
            message = "add"
        return response.Response(
            data={"message": f"Success {message} course to interest"},
            status=status.HTTP_200_OK,
        )


class AddCourseToWantedPassingView(APIView):
    """View for course to ``wanted passing`` by some user."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=self.request.user.pk)
        if user in course.students.all():
            message = ""
            if user in course.want_pass_users.all():
                course.want_pass_users.remove(user)
                message = "remove"
            else:
                course.want_pass_users.add(user)
                message = "add"
            return response.Response(
                data={"message": f"Success {message} course to wanted-passing"},
                status=status.HTTP_200_OK,
            )
        return response.Response(
            data={
                "message": "User is not in students of course",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class AddCourseToAchiveView(APIView):
    """View for course to achive by some user."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=self.request.user.pk)
        if user in course.students.all():
            message = ""
            if user in course.archive_users.all():
                course.archive_users.remove(user)
                message = "remove"
            else:
                course.archive_users.add(user)
                message = "add"
            return response.Response(
                data={"message": f"Success {message} course to achive"},
                status=status.HTTP_200_OK,
            )
        return response.Response(
            data={
                "message": "User is not in students of course",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class TopicViewSet(views.SimpleBaseViewSet):
    """ViewSet for Topic model."""

    serializer_class = serializers.TopicSerializer
    queryset = models.Topic.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)


class TaskViewSet(views.SimpleBaseViewSet):
    """ViewSet for Task model."""

    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)


class AnswerViewSet(views.SimpleBaseViewSet):
    """ViewSet for Answer model."""

    serializer_class = serializers.AnswerSerializer
    queryset = models.Answer.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)


class CommentViewSet(views.SimpleBaseViewSet):
    """ViewSet for Comment model."""

    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    permission_classes = (permissions.IsCreatorOrStudent,)

    def perform_create(self, serializer) -> None:
        """Overriden for create instanse and get User instanse from request."""
        serializer.save(user=self.request.user)


class ReviewViewSet(views.SimpleBaseViewSet):
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
    permission_classes = (permis.AllowAny,)


class CategoryAPIView(generics.RetrieveAPIView):
    """APIView for get instanse of Category model."""

    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = (permis.AllowAny,)
