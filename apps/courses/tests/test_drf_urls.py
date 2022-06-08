from rest_framework import status


def test_permission_failed(api_client):
    """Test unauthentication user."""
    assert (
        api_client.get("/api/v1/courses/").status_code == status.HTTP_401_UNAUTHORIZED
    )


def test_permission_success(api_client_auth):
    """Test authentication user."""
    assert api_client_auth.get("/api/v1/courses/").status_code == status.HTTP_200_OK
