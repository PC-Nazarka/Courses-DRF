import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_user_detail(user):
    assert (
        reverse("api:user-detail", kwargs={"pk": user.id})
        == f"/api/v1/users/{user.id}/"
    )
    assert resolve(f"/api/v1/users/{user.id}/").view_name == "api:user-detail"


def test_user_list():
    assert reverse("api:user-list") == "/api/v1/users/"
    assert resolve("/api/v1/users/").view_name == "api:user-list"
