from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.models import BaseModel


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="Deleted")[0]


class Review(BaseModel):
    "Model for Review."

    rating = models.IntegerField(
        verbose_name=_("Mark of course by user"),
    )
    review = models.TextField(
        verbose_name=_("Review of course by user"),
    )
    user = models.ForeignKey(
        "apps.users.User",
        on_delete=models.SET(get_sentinel_user),
        verbose_name=_("Owner of review"),
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        verbose_name=_("Reviews of courses"),
        related_name="reviews",
    )

    class Meta:
        verbose_name_plural = _("Reviews")
        verbose_name = _("Review")
