from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom model for User."""

    description = models.TextField(
        verbose_name=_("Description of user"),
    )
