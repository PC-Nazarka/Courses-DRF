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
        "courses/<int:pk>/add-interest/",
        views.AddCourseToInterestView.as_view(),
        name="add-interest",
    ),
    path(
        "courses/<int:pk>/add-wanted-passing/",
        views.AddCourseToWantedPassingView.as_view(),
        name="add-wanted-passing",
    ),
    path(
        "courses/<int:pk>/add-achive/",
        views.AddCourseToAchiveView.as_view(),
        name="add-achive",
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
