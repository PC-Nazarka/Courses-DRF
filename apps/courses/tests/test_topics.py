import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.courses import factories, models
from apps.users.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_create_topic(
    user,
    api_client,
) -> None:
    """Test topic creation."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.build()
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:topic-list"),
        data={
            "title": topic.title,
            "number": topic.number,
            "course": course.id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Topic.objects.filter(
        title=topic.title,
        number=topic.number,
        course=course.id,
    ).exists()


def test_owner_update_topic(
    user,
    api_client,
) -> None:
    """Test update topic by owner."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    new_name = "My topic"
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse_lazy("api:topic-detail", kwargs={"pk": topic.pk}),
        data={
            "title": new_name,
            "number": topic.number,
            "course": course.id,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert models.Topic.objects.filter(
        title=new_name,
        number=topic.number,
        course=course.id,
    ).exists()


def test_not_owner_update_topic(
    user,
    api_client,
) -> None:
    """Test update topic by another user."""
    another_user = UserFactory.create()
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    new_name = "My topic"
    api_client.force_authenticate(user=another_user)
    response = api_client.put(
        reverse_lazy("api:topic-detail", kwargs={"pk": topic.pk}),
        data={
            "title": new_name,
            "number": topic.number,
            "course": course.id,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_remove_topic(
    user,
    api_client,
) -> None:
    """Test remove topic by owner."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    api_client.force_authenticate(user=user)
    api_client.delete(
        reverse_lazy("api:topic-detail", kwargs={"pk": topic.pk}),
    )
    assert topic not in models.Topic.objects.all()


def test_not_owner_remove_topic(
    user,
    api_client,
) -> None:
    """Test remove topic by another user."""
    another_user = UserFactory.create()
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    topic = factories.TopicFactory.create(
        course=course,
    )
    api_client.force_authenticate(user=another_user)
    response = api_client.delete(
        reverse_lazy("api:topic-detail", kwargs={"pk": topic.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
