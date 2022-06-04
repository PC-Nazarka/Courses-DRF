import pytest
from rest_framework import test
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(django_db_setup, django_db_blocker):
    """Module-level fixture for user."""
    with django_db_blocker.unblock():
        created_user = UserFactory()
        yield created_user
        created_user.delete()


@pytest.fixture
def auth_client(user, client):
    """Fixture for authtorized client."""
    client.force_login(user=user)
    return client


@pytest.fixture
def api_client() -> test.APIClient:
    """Create api client."""
    return test.APIClient()


@pytest.fixture
def api_client_auth(user):
    """Fixture for authtorized api client with JWT."""
    client = test.APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"JWT {refresh.access_token}")
    return client
