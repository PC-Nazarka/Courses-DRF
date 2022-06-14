from django.urls import include, path

from . import views

app_name = "user"
urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
