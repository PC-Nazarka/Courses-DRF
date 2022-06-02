import pytest
from django.test import RequestFactory

from apps.users.views import UserViewSet

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self, user, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()
