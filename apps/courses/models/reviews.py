from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from .courses import get_sentinel_user


class Review(BaseModel):
    "Model for Review."

    rating = models.IntegerField(
        verbose_name=_("Mark of course by user"),
    )
    review = models.TextField(
        verbose_name=_("Review of course by user"),
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET(get_sentinel_user),
        verbose_name=_("Owner of review"),
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        verbose_name=_("Reviews of courses"),
        related_name="reviews",
    )

    def __str__(self) -> str:
        """String representation of object."""
        return f"Review {self.rating}, review {self.review[:10]}"

    class Meta:
        verbose_name_plural = _("Reviews")
        verbose_name = _("Review")
