from django.urls import path

from . import views

app_name = "courses"
urlpatterns = [
    path(
        "courses/<int:pk>/add-student/",
        views.AddStudentsToCourseView.as_view(),
        name="add-students",
    )
]
