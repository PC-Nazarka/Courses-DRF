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


class IsCreatorOrStudent(permissions.BasePermission):
    """Custom permission for let change object by creator or student."""

    def has_permission(self, request, view) -> bool:
        """Overriden for differentiate simple user and creator.

        Student of course can read all model, but create can only comment and
        review.
        Creator can create all and read all.
        """
        if view.basename in ("course", "topic", "task", "answer"):
            if request.method == "GET":
                if all(
                    [
                        "pk" not in request.parser_context["kwargs"],
                        view.basename == "course",
                    ]
                ):
                    return True

            if request.method == "POST":
                if view.basename in ("topic", "task", "answer"):
                    course = get_course_instanse(request.data)
                    return request.user.id == course.owner.id
                return True

            data = {view.basename: request.parser_context["kwargs"]["pk"]}
            course = get_course_instanse(data)
            if request.method == "GET":
                if view.basename in ("course", "topic"):
                    return any(
                        [
                            course.owner.id == request.user.id,
                            course.status == models.Course.Status.READY,
                            all(
                                [
                                    course.status == models.Course.Status.READY,
                                    request.user in course.students.all(),
                                ]
                            ),
                        ]
                    )
                return any(
                    [
                        request.user.id == course.owner.id,
                        all(
                            [
                                course.status == models.Course.Status.READY,
                                request.user in course.students.all(),
                            ]
                        ),
                    ]
                )

            if request.method in ("PUT", "PATCH", "DELETE"):
                return request.user.id == course.owner.id

        if view.basename in ("comment", "review"):
            if request.method == "POST":
                course = get_course_instanse(request.data)
                return any(
                    [
                        request.user.id == course.owner.id,
                        all(
                            [
                                request.user in course.students.all(),
                                course.status == models.Course.Status.READY,
                            ]
                        ),
                    ]
                )

            data = {view.basename: request.parser_context["kwargs"]["pk"]}
            course = get_course_instanse(data)
            if request.method in ("PUT", "PATCH", "DELETE", "GET"):
                return any(
                    [
                        request.user.id == course.owner.id,
                        all(
                            [
                                request.user in course.students.all(),
                                course.status == models.Course.Status.READY,
                            ]
                        ),
                    ]
                )
