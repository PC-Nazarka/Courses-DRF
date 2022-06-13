from django.db.models import Q
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

    def search_queryset(self, object_list):
        """Filter queryset by search query."""
        query_search = self.request.GET.get("search")
        if query_search:
            return object_list.filter(
                Q(name__icontains=query_search)
                | Q(description__icontains=query_search),
            )
        return object_list

    def filter_queryset(self, object_list):
        """Filter queryset by filter query."""
        query_filter = self.request.GET.get("price")
        if query_filter:
            return object_list.filter(price=query_filter)
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
        object_list = models.Course.objects.all()
        object_list = self.search_queryset(object_list)
        object_list = self.filter_queryset(object_list)
        object_list = self.category_queryset(object_list)
        return object_list


class AddStudentsToCourseView(generics.GenericAPIView):
    """View for add student to course."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=request.user.pk)
        message = ""
        if user in course.students.all():
            course.students.remove(user)
            message = "remove"
        else:
            course.students.add(user)
            message = "add"
        return response.Response(
            data={"message": f"Success {message} students to course"},
            status=status.HTTP_200_OK,
        )


class AddCourseToPassingView(generics.GenericAPIView):
    """View for course to passing by some user."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=self.request.user.pk)
        message = ""
        if user in course.passers_users.all():
            course.passers_users.remove(user)
            message = "remove"
        else:
            course.passers_users.add(user)
            message = "add"
        return response.Response(
            data={"message": f"Success {message} course to passing"},
            status=status.HTTP_200_OK,
        )


class AddCourseToInterestView(generics.GenericAPIView):
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


class AddCourseToWantedPassingView(generics.GenericAPIView):
    """View for course to ``wanted passing`` by some user."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=self.request.user.pk)
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


class AddCourseToAchiveView(generics.GenericAPIView):
    """View for course to achive by some user."""

    def post(self, request, *args, **kwargs):
        """Handler POST request."""
        course = models.Course.objects.get(pk=self.kwargs["pk"])
        user = User.objects.get(pk=self.request.user.pk)
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


class FilterCoursesView(generics.ListAPIView):
    """View for filter courses."""

    def search_queryset(self, object_list):
        """Filter queryset by search query."""
        query_search = self.request.GET.get("search")
        if query_search:
            return object_list.filter(
                Q(name__icontains=query_search)
                | Q(description__icontains=query_search),
            )
        return query_search

    def filter_queryset(self, object_list):
        """Filter queryset by filter query."""
        query_filter = self.request.GET.get("price")
        print(query_filter)
        if query_filter:
            return object_list.filter(price=query_filter)
        return object_list

    def category_queryset(self, object_list):
        """Filter queryset by cateofry query."""
        query_category = self.request.GET.get("category")
        if query_category:
            return object_list.filter(
                category__id=models.Category.objects.get(
                    pk=int(query_category),
                ),
            )
        return object_list

    def get_queryset(self):
        """Get search result."""
        object_list = models.Course.objects.all()
        print(object_list)
        object_list = self.get_search_queryset(object_list)
        object_list = self.get_filter_queryset(object_list)
        object_list = self.get_category_queryset(object_list)
        return object_list


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
