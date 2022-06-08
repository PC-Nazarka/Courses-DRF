import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_user_detail(user):
    """Check view name of detail users."""
    assert (
        reverse("user:user-detail", kwargs={"id": user.id})
        == f"/api/v1/auth/users/{user.id}/"
    )
    assert resolve(f"/api/v1/auth/users/{user.id}/").view_name == "user:user-detail"


def test_user_list():
    """Check view name of list users."""
    assert reverse("user:user-list") == "/api/v1/auth/users/"
    assert resolve("/api/v1/auth/users/").view_name == "user:user-list"
