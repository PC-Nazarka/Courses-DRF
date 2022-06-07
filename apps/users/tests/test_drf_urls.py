import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_user_detail(user):
    assert (
        reverse("user:user-detail", kwargs={"id": user.id})
        == f"/api/v1/auth/users/{user.id}/"
    )
    assert resolve(f"/api/v1/auth/users/{user.id}/").view_name == "user:user-detail"


def test_user_list():
    assert reverse("user:user-list") == "/api/v1/auth/users/"
    assert resolve("/api/v1/auth/users/").view_name == "user:user-list"
