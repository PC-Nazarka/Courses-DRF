import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_user_detail(user):
    assert (
        reverse("api:user-detail", kwargs={"pk": user.id}) == f"/api/users/{user.id}/"
    )
    assert resolve(f"/api/users/{user.id}/").view_name == "api:user-detail"


def test_user_list():
    assert reverse("api:user-list") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:user-list"
