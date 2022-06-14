from rest_framework import permissions

from . import models, serializers


def get_course_instanse(data: dict) -> models.Course:
    """In dependencies of data get `Course` instanse."""
    if "task" in data:
        task_json = serializers.TaskSerializer(
            models.Task.objects.get(pk=data["task"]),
        ).data
        return get_course_instanse(task_json)
    if "topic" in data:
        topic_json = serializers.TopicSerializer(
            models.Topic.objects.get(pk=data["topic"]),
        ).data
        return get_course_instanse(topic_json)
    if "course" in data:
        return models.Course.objects.get(pk=data["course"])


def course_is_ready(view, request) -> bool:
    """Check status of course.

    If page of list of courses - return True, else if page of one course -
    check status.
    """
    if view.basename == "topic":
        data = serializers.TopicSerializer(
            models.Topic.objects.get(
                pk=request.parser_context["kwargs"]["pk"],
            ),
        ).data
        course = get_course_instanse(data)
        if course.owner.id == request.user.id:
            return True
        return course.status == models.Course.Status.READY

    if "pk" in request.parser_context["kwargs"]:
        course = models.Course.objects.get(
            pk=request.parser_context["kwargs"]["pk"],
        )
        if course.owner.id == request.user.id:
            return True
        return course.status == models.Course.Status.READY

    return True


class IsCreatorOrStudent(permissions.BasePermission):
    """Custom permission for let change object by creator or student."""

    def has_permission(self, request, view) -> bool:
        """Overriden for differentiate simple user and creator.

        Student of course can read all model, but create can only comment and
        review.
        Creator can create all and read all.
        """
        if view.basename in ("course", "topic", "task", "answer"):
            course = None
            if request.method == "POST":
                if view.basename != "course":
                    course = get_course_instanse(request.data)
                    return request.user.id == course.owner.id
                return True

            if request.method == "GET":
                if view.basename in ("course", "topic"):
                    return course_is_ready(view, request)
                return any(
                    [
                        request.user.id == course.owner.id,
                        request.user in course.students.all(),
                    ]
                )

            data = {}
            match view.basename:
                case "answer":
                    data = serializers.AnswerSerializer(
                        models.Answer.objects.get(
                            pk=request.parser_context["kwargs"]["pk"],
                        ),
                    ).data
                case "task":
                    data = serializers.TaskSerializer(
                        models.Task.objects.get(
                            pk=request.parser_context["kwargs"]["pk"],
                        ),
                    ).data
                case "topic":
                    data = serializers.TopicSerializer(
                        models.Topic.objects.get(
                            pk=request.parser_context["kwargs"]["pk"],
                        ),
                    ).data
                case "course":
                    course = models.Course.objects.get(
                        pk=request.parser_context["kwargs"]["pk"],
                    )
            if not course:
                course = get_course_instanse(data)
            if request.method in ("PUT", "PATCH", "DELETE"):
                return request.user.id == course.owner.id

        if view.basename in ("comment", "review"):
            if request.method == "POST":
                course = get_course_instanse(request.data)
                return any(
                    [
                        request.user.id == course.owner.id,
                        request.user in course.students.all(),
                    ]
                )

            data = {}
            match view.basename:
                case "review":
                    data = serializers.ReviewSerializer(
                        models.Review.objects.get(
                            pk=request.parser_context["kwargs"]["pk"],
                        ),
                    ).data
                case "comment":
                    data = serializers.CommentSerializer(
                        models.Comment.objects.get(
                            pk=request.parser_context["kwargs"]["pk"],
                        ),
                    ).data
            course = get_course_instanse(data)
            if request.method in ("PUT", "PATCH", "DELETE", "GET"):
                return any(
                    [
                        request.user.id == course.owner.id,
                        request.user in course.students.all(),
                    ]
                )
