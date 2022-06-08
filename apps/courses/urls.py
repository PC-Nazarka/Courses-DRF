from django.urls import path

from . import views

app_name = "courses"
urlpatterns = [
    path(
        "courses/<int:pk>/add-student/",
        views.AddStudentsToCourseView.as_view(),
        name="add-students",
    ),
    path(
        "categories/",
        views.CategoryListAPIView.as_view(),
        name="list-categories",
    ),
    path(
        "categories/<int:pk>/",
        views.CategoryAPIView.as_view(),
        name="category-object",
    ),
]
