from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.courses.views import (
    AnswerViewSet,
    CommentViewSet,
    CourseViewSet,
    ReviewViewSet,
    TaskViewSet,
    TopicViewSet,
)

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("courses", CourseViewSet, basename="course")
router.register("topics", TopicViewSet, basename="topic")
router.register("tasks", TaskViewSet, basename="task")
router.register("answers", AnswerViewSet, basename="answer")
router.register("comments", CommentViewSet, basename="comment")
router.register("reviews", ReviewViewSet, basename="review")

app_name = "api"
urlpatterns = router.urls
