import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.courses import factories, models

pytestmark = pytest.mark.django_db


def test_create_answer_by_user_by_student(
    user,
    api_client,
) -> None:
    """Test create answer by user by student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    course.students.add(user)
    answer_by_user = factories.AnswerByUserFactory.build(
        user=user,
        task=task,
    )
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:answer-by-user-list"),
        data={
            "task": answer_by_user.task.id,
            "user": answer_by_user.user.id,
            "answer": answer_by_user.answer,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.AnswerByUser.objects.filter(
        task=answer_by_user.task.id,
        user=answer_by_user.user.id,
        answer=answer_by_user.answer,
    ).exists()


def test_create_answer_by_user_by_not_student(
    user,
    api_client,
) -> None:
    """Test create answer by user by not student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer_by_user = factories.AnswerByUserFactory.build(
        user=user,
        task=task,
    )
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:answer-by-user-list"),
        data={
            "task": answer_by_user.task.id,
            "user": answer_by_user.user.id,
            "answer": answer_by_user.answer,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_answer_by_user_by_student(
    user,
    api_client,
) -> None:
    """Test read answer by user by student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer_by_user = factories.AnswerByUserFactory.create(
        user=user,
        task=task,
    )
    course.students.add(user)
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy(
            "api:answer-by-user-detail",
            kwargs={"pk": answer_by_user.task.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_answer_by_user_by_owner(
    user,
    api_client,
) -> None:
    """Test read answer by user by owner of course."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer_by_user = factories.AnswerByUserFactory.create(
        user=user,
        task=task,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy(
            "api:answer-by-user-detail",
            kwargs={"pk": answer_by_user.task.pk},
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_read_answer_by_user_by_not_student(
    user,
    api_client,
) -> None:
    """Test read answer by user by not student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer_by_user = factories.AnswerByUserFactory.create(
        user=user,
        task=task,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy(
            "api:answer-by-user-detail",
            kwargs={"pk": answer_by_user.task.pk},
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_read_answer_by_user_by_not_auth(
    user,
    api_client,
) -> None:
    """Test read answer by user by not auth."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer_by_user = factories.AnswerByUserFactory.create(
        user=user,
        task=task,
    )
    response = api_client.get(
        reverse_lazy(
            "api:answer-by-user-detail",
            kwargs={"pk": answer_by_user.task.pk},
        ),
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_answer_by_user_by_student(
    user,
    api_client,
) -> None:
    """Test update answer by user by student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer_by_user = factories.AnswerByUserFactory.create(
        user=user,
        task=task,
    )
    course.students.add(user)
    api_client.force_authenticate(user=user)
    answer = not answer_by_user.answer
    response = api_client.put(
        reverse_lazy(
            "api:answer-by-user-detail",
            kwargs={"pk": answer_by_user.task.pk},
        ),
        data={
            "task": answer_by_user.task.id,
            "user": answer_by_user.user.id,
            "answer": answer,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert models.AnswerByUser.objects.filter(
        task=answer_by_user.task.id,
        user=answer_by_user.user.id,
        answer=answer,
    ).exists()
