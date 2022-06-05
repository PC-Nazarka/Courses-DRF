from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoursesConfig(AppConfig):
    """Class-configuration of courses app."""

    name = "apps.courses"
    verbose_name = _("Courses")
