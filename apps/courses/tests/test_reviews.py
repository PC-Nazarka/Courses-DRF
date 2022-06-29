import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.courses import factories, models

pytestmark = pytest.mark.django_db


def test_create_review_by_student(
    user,
    api_client,
) -> None:
    """Test review creation by student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    course.students.add(user)
    review = factories.ReviewFactory.build()
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:review-list"),
        data={
            "rating": review.rating,
            "review": review.review,
            "course": course.id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Review.objects.filter(
        rating=review.rating,
        review=review.review,
        course=course.id,
        user=user.id,
    ).exists()


def test_create_review_by_not_student(
    user,
    api_client,
) -> None:
    """Test review creation by not student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    review = factories.ReviewFactory.build()
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:review-list"),
        data={
            "rating": review.rating,
            "review": review.review,
            "course": course.id,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_update_review(
    user,
    api_client,
) -> None:
    """Test update review by owner."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    course.students.add(user)
    review = factories.ReviewFactory.create(
        user=user,
        course=course,
    )
    new_name = "My review"
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse_lazy("api:review-detail", kwargs={"pk": review.pk}),
        data={
            "review": new_name,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert models.Review.objects.filter(
        review=new_name,
        rating=review.rating,
        course=course.id,
        user=user.id,
    ).exists()


def test_not_owner_update_review(
    user,
    api_client,
) -> None:
    """Test update review by another user."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    review = factories.ReviewFactory.create(
        course=course,
    )
    new_name = "My review"
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse_lazy("api:review-detail", kwargs={"pk": review.pk}),
        data={
            "review": new_name,
            "rating": review.rating,
            "course": course.id,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_remove_review(
    user,
    api_client,
) -> None:
    """Test remove review by owner."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    course.students.add(user)
    review = factories.ReviewFactory.create(
        user=user,
        course=course,
    )
    api_client.force_authenticate(user=user)
    api_client.delete(
        reverse_lazy("api:review-detail", kwargs={"pk": review.pk}),
    )
    assert review not in models.Task.objects.all()


def test_not_owner_remove_review(
    user,
    api_client,
) -> None:
    """Test remove review by another user."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    review = factories.ReviewFactory.create(
        course=course,
    )
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse_lazy("api:review-detail", kwargs={"pk": review.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_not_student_read_review(
    user,
    api_client,
) -> None:
    """Test read review by not student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    review = factories.ReviewFactory.create(
        course=course,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy("api:review-detail", kwargs={"pk": review.pk}),
    )
    assert response.status_code == status.HTTP_200_OK


def test_student_read_review(
    user,
    api_client,
) -> None:
    """Test read review by student."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    review = factories.ReviewFactory.create(
        course=course,
    )
    course.students.add(user)
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy("api:review-detail", kwargs={"pk": review.pk}),
    )
    assert response.status_code == status.HTTP_200_OK


def test_not_auth_read_review(
    api_client,
) -> None:
    """Test read review by not auth user."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    review = factories.ReviewFactory.create(
        course=course,
    )
    response = api_client.get(
        reverse_lazy("api:review-detail", kwargs={"pk": review.pk}),
    )
    assert response.status_code == status.HTTP_200_OK


def test_auth_read_review(
    user,
    api_client,
) -> None:
    """Test read review by not auth user."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
    )
    review = factories.ReviewFactory.create(
        course=course,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy("api:review-detail", kwargs={"pk": review.pk}),
    )
    assert response.status_code == status.HTTP_200_OK


def test_owner_course_read_review(
    user,
    api_client,
) -> None:
    """Test read review by not auth user."""
    course = factories.CourseFactory.create(
        status=models.Course.Status.READY,
        owner=user,
    )
    review = factories.ReviewFactory.create(
        course=course,
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse_lazy("api:review-detail", kwargs={"pk": review.pk}),
    )
    assert response.status_code == status.HTTP_200_OK
