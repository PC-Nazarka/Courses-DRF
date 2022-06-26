import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.courses import factories, models
from apps.users.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_create_task(
    user,
    api_client,
) -> None:
    """Test task creation."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    task = factories.TaskFactory.build()
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:task-list"),
        data={
            "type_task": task.type_task,
            "title": task.title,
            "text": task.text,
            "topic": topic.id,
            "number": task.number,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Task.objects.filter(
        type_task=task.type_task,
        title=task.title,
        text=task.text,
        topic=topic.id,
        number=task.number,
    ).exists()


def test_owner_update_task(
    user,
    api_client,
) -> None:
    """Test update task by owner."""
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
    new_name = "My task"
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse_lazy("api:task-detail", kwargs={"pk": task.pk}),
        data={
            "type_task": task.type_task,
            "title": new_name,
            "text": task.text,
            "topic": topic.id,
            "number": task.number,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert models.Task.objects.filter(
        type_task=task.type_task,
        title=new_name,
        text=task.text,
        topic=topic.id,
        number=task.number,
    ).exists()


def test_not_owner_update_task(
    user,
    api_client,
) -> None:
    """Test update task by another user."""
    another_user = UserFactory.create()
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
    new_name = "My task"
    api_client.force_authenticate(user=another_user)
    response = api_client.put(
        reverse_lazy("api:task-detail", kwargs={"pk": task.pk}),
        data={
            "type_task": new_name,
            "title": task.title,
            "text": task.text,
            "topic": topic.id,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_remove_task(
    user,
    api_client,
) -> None:
    """Test remove task by owner."""
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
    api_client.force_authenticate(user=user)
    api_client.delete(
        reverse_lazy("api:task-detail", kwargs={"pk": task.pk}),
    )
    assert task not in models.Task.objects.all()


def test_not_owner_remove_task(
    user,
    api_client,
) -> None:
    """Test remove task by another user."""
    another_user = UserFactory.create()
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
    api_client.force_authenticate(user=another_user)
    response = api_client.delete(
        reverse_lazy("api:task-detail", kwargs={"pk": task.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
