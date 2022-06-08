import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.courses import factories, models
from apps.users.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_create_answer(
    user,
    api_client,
) -> None:
    """Test answer creation."""
    course = factories.CourseFactory.create(
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer = factories.AnswerFactory.build()
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:answer-list"),
        data={
            "is_true": answer.is_true,
            "content": answer.content,
            "task": task.id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Answer.objects.filter(
        is_true=answer.is_true,
        content=answer.content,
        task=task.id,
    ).exists()


def test_owner_update_answer(
    user,
    api_client,
) -> None:
    """Test update answer by owner."""
    course = factories.CourseFactory.create(
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer = factories.AnswerFactory.create(
        task=task,
    )
    api_client.force_authenticate(user=user)
    new_content = "My answer"
    response = api_client.put(
        reverse_lazy(
            "api:answer-detail",
            kwargs={"pk": answer.pk},
        ),
        data={
            "is_true": answer.is_true,
            "content": new_content,
            "task": answer.task.id,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert models.Answer.objects.filter(
        is_true=answer.is_true,
        content=new_content,
        task=answer.task.id,
    ).exists()


def test_not_owner_update_answer(
    user,
    api_client,
) -> None:
    """Test update answer by another user."""
    another_user = UserFactory.create()
    course = factories.CourseFactory.create(
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer = factories.AnswerFactory.create(
        task=task,
    )
    api_client.force_authenticate(user=another_user)
    new_content = "My answer"
    response = api_client.put(
        reverse_lazy(
            "api:answer-detail",
            kwargs={"pk": answer.pk},
        ),
        data={
            "is_true": answer.is_true,
            "content": new_content,
            "task": answer.task.id,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_remove_answer(
    user,
    api_client,
) -> None:
    """Test remove answer by owner."""
    course = factories.CourseFactory.create(
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer = factories.AnswerFactory.create(
        task=task,
    )
    api_client.force_authenticate(user=user)
    api_client.delete(
        reverse_lazy(
            "api:answer-detail",
            kwargs={"pk": answer.pk},
        ),
        data={
            "is_true": answer.is_true,
            "content": answer.content,
            "task": answer.task.id,
        },
    )
    assert answer not in models.Answer.objects.all()


def test_not_owner_remove_answer(
    user,
    api_client,
) -> None:
    """Test remove answer by another user."""
    another_user = UserFactory.create()
    course = factories.CourseFactory.create(
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.create(
        topic=topic,
    )
    answer = factories.AnswerFactory.create(
        task=task,
    )
    api_client.force_authenticate(user=another_user)
    response = api_client.delete(
        reverse_lazy(
            "api:answer-detail",
            kwargs={"pk": answer.pk},
        ),
        data={
            "is_true": answer.is_true,
            "content": answer.content,
            "task": answer.task.id,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
