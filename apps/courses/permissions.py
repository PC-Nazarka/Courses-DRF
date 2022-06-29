from rest_framework import permissions

from . import models, serializers


def get_course_instanse(data: dict) -> models.Course:
    """In dependencies of data get `Course` instanse."""
    if "course" in data:
        return models.Course.objects.get(pk=data["course"])
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
    if "answer" in data:
        answer_json = serializers.AnswerSerializer(
            models.Answer.objects.get(pk=data["answer"]),
        ).data
        return get_course_instanse(answer_json)
    if "comment" in data:
        comment_json = serializers.CommentSerializer(
            models.Comment.objects.get(pk=data["comment"]),
        ).data
        return get_course_instanse(comment_json)
    if "review" in data:
        review_json = serializers.ReviewSerializer(
            models.Review.objects.get(pk=data["review"]),
        ).data
        return get_course_instanse(review_json)
    if "answer-by-user" in data:
        answer_by_user = serializers.AnswerByUserSerializer(
            models.AnswerByUser.objects.get(pk=data["answer-by-user"]),
        ).data
        return get_course_instanse(answer_by_user)


def get_view(view):
    return "task" if view.basename == "answer-by-user" else view.basename


class IsStudent(permissions.BasePermission):
    """Custom permission for let change object by student of course."""

    def has_permission(self, request, view) -> bool:
        """Overriden for different student of course and simple user."""
        match view.basename:
            case "course":
                if request.method in ("GET", "POST"):
                    return True
                if request.method in ("DELETE", "PUT", "PATCH"):
                    return False
            case "topic":
                if request.method in ("POST", "DELETE", "PUT", "PATCH"):
                    return False
                return True
            case "task" | "answer":
                if bool(request.user and request.user.is_authenticated):
                    if request.method in ("POST", "DELETE", "PUT", "PATCH"):
                        return False
                    data = {view.basename: request.parser_context["kwargs"]["pk"]}
                    course = get_course_instanse(data)
                    return all(
                        [
                            request.user in course.students.all(),
                            course.status == models.Course.Status.READY,
                        ],
                    )
            case "comment":
                if bool(request.user and request.user.is_authenticated):
                    if request.method in ("GET", "POST"):
                        data = (
                            request.data
                            if request.method == "POST"
                            else {view.basename: request.parser_context["kwargs"]["pk"]}
                        )
                        course = get_course_instanse(data)
                        return all(
                            [
                                request.user in course.students.all(),
                                course.status == models.Course.Status.READY,
                            ],
                        )
                    if request.method in ("DELETE", "PUT", "PATCH"):
                        comment = models.Comment.objects.get(
                            id=request.parser_context["kwargs"]["pk"]
                        )
                        data = {view.basename: request.parser_context["kwargs"]["pk"]}
                        course = get_course_instanse(data)
                        return all(
                            [
                                request.user in course.students.all(),
                                course.status == models.Course.Status.READY,
                                comment.user == request.user,
                            ],
                        )
            case "review":
                if request.method == "GET":
                    return True
                if request.method == "POST":
                    course = get_course_instanse(request.data)
                    return all(
                        [
                            request.user in course.students.all(),
                            course.status == models.Course.Status.READY,
                        ],
                    )
                if request.method in ("DELETE", "PUT", "PATCH"):
                    review = models.Review.objects.get(
                        id=request.parser_context["kwargs"]["pk"],
                    )
                    data = {view.basename: request.parser_context["kwargs"]["pk"]}
                    course = get_course_instanse(data)
                    return all(
                        [
                            request.user in course.students.all(),
                            course.status == models.Course.Status.READY,
                            review.user == request.user,
                        ],
                    )
            case "answer-by-user":
                if bool(request.user and request.user.is_authenticated):
                    data = (
                        request.data
                        if request.method == "POST"
                        else {get_view(view): request.parser_context["kwargs"]["pk"]}
                    )
                    course = get_course_instanse(data)
                    return all(
                        [
                            request.user in course.students.all(),
                            course.status == models.Course.Status.READY,
                        ],
                    )


class IsOwner(permissions.BasePermission):
    """Custom permission for let change object by owner of course."""

    def has_permission(self, request, view) -> bool:
        """Overriden for different owner of course and simple user."""
        match view.basename:
            case "course":
                if request.method in ("GET", "POST"):
                    return True
                if request.method in ("DELETE", "PUT", "PATCH"):
                    data = {get_view(view): request.parser_context["kwargs"]["pk"]}
                    course = get_course_instanse(data)
                    return course.owner == request.user
            case "topic":
                if request.method in ("POST", "DELETE", "PUT", "PATCH"):
                    data = (
                        request.data
                        if request.method == "POST"
                        else {get_view(view): request.parser_context["kwargs"]["pk"]}
                    )
                    course = get_course_instanse(data)
                    return course.owner == request.user
                return True
            case "task" | "answer":
                if bool(request.user and request.user.is_authenticated):
                    data = (
                        request.data
                        if request.method == "POST"
                        else {get_view(view): request.parser_context["kwargs"]["pk"]}
                    )
                    course = get_course_instanse(data)
                    return course.owner == request.user
            case "comment":
                if bool(request.user and request.user.is_authenticated):
                    if request.method in ("GET", "POST"):
                        data = (
                            request.data
                            if request.method == "POST"
                            else {
                                get_view(view): request.parser_context["kwargs"]["pk"]
                            }
                        )
                        course = get_course_instanse(data)
                        return course.owner == request.user
                    if request.method in ("DELETE", "PUT", "PATCH"):
                        comment = models.Comment.objects.get(
                            id=request.parser_context["kwargs"]["pk"]
                        )
                        data = {get_view(view): request.parser_context["kwargs"]["pk"]}
                        course = get_course_instanse(data)
                        return course.owner == request.user == comment.user
            case "review":
                if request.method == "GET":
                    return True
                if request.method == "POST":
                    course = get_course_instanse(request.data)
                    return course.owner == request.user
                if request.method in ("DELETE", "PUT", "PATCH"):
                    review = models.Review.objects.get(
                        id=request.parser_context["kwargs"]["pk"],
                    )
                    data = {get_view(view): request.parser_context["kwargs"]["pk"]}
                    course = get_course_instanse(data)
                    return review.user == request.user == course.owner
            case "answer-by-user":
                if bool(request.user and request.user.is_authenticated):
                    if request.method in ("GET", "POST"):
                        data = (
                            request.data
                            if request.method == "POST"
                            else {
                                get_view(view): request.parser_context["kwargs"]["pk"]
                            }
                        )
                        course = get_course_instanse(data)
                        return course.owner == request.user
                    if request.method in ("DELETE", "PUT", "PATCH"):
                        answer = models.AnswerByUser.objects.get(
                            task_id=request.parser_context["kwargs"]["pk"]
                        )
                        data = {get_view(view): request.parser_context["kwargs"]["pk"]}
                        course = get_course_instanse(data)
                        return course.owner == request.user == answer.user
