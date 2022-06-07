from django.urls import include, path

app_name = "user"
urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("rest_framework_social_oauth2.urls")),
]
