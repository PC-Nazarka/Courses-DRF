from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


def get_directory_path(instance, _) -> str:
    """Get directory for save image of course."""
    return f"course_{instance.name}_{instance.id}"


def get_sentinel_user():
    """Get ``deleted`` user."""
    return get_user_model().objects.get_or_create(username="Deleted")[0]


class Course(BaseModel):
    """Model for Course."""

    name = models.CharField(
        max_length=128,
        verbose_name=_("Name of course"),
    )
    description = models.TextField(
        verbose_name=_("Description of course"),
    )
    image = models.ImageField(
        upload_to=get_directory_path,
        verbose_name=_("Image of course"),
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=11,
        verbose_name=_("Price of course"),
        default=Decimal("0.0"),
    )
    students = models.ManyToManyField(
        "users.User",
        verbose_name=_("One of students"),
        related_name="courses_student",
    )
    passers_users = models.ManyToManyField(
        "users.User",
        verbose_name=_("Passes users"),
        related_name="pass_courses",
    )
    interest_users = models.ManyToManyField(
        "users.User",
        verbose_name=_("Users mean, that this course is interesting"),
        related_name="favorite_courses",
    )
    want_pass_users = models.ManyToManyField(
        "users.User",
        verbose_name=_("Users who want pass course"),
        related_name="want_pass_courses",
    )
    archive_users = models.ManyToManyField(
        "users.User",
        verbose_name=_("Users who add course in archive"),
        related_name="archive_courses",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name=_("Category of course"),
        related_name="courses",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name=_("Owner of course"),
        related_name="courses",
    )

    def __str__(self) -> str:
        """String representation of object."""
        return f"Course {self.name}"

    class Meta:
        verbose_name_plural = _("Courses")
        verbose_name = _("Course")


class Category(BaseModel):
    """Model for Category."""

    name = models.CharField(
        max_length=128,
        verbose_name=_("Name of category"),
    )

    def __str__(self) -> str:
        """String representation of object."""
        return f"Category {self.name}"

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _("Category")


class Topic(BaseModel):
    """Model for Topic."""

    title = models.CharField(
        max_length=255,
        verbose_name=_("One title of topic"),
    )
    number = models.IntegerField(
        verbose_name=_("Number topic in course"),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Course for topic"),
        related_name="topics",
    )

    def __str__(self) -> str:
        """String representation of object."""
        return f"Topic {self.title}, number {self.number}"

    class Meta:
        verbose_name_plural = _("Topics")
        verbose_name = _("Topic")


class Task(BaseModel):
    """Model for Task.

    Task types:
        Information: in body of task exist only some information
        Test: in body of task exist information and questions
    """

    class TypeTask(models.TextChoices):
        """Class choices."""

        INFORMATION = "INFORMATION", _("Information")
        TEST = "TEST", _("Test")

    type_task = models.CharField(
        max_length=255,
        verbose_name=_("Type"),
        choices=TypeTask.choices,
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("One title of task"),
    )
    text = models.TextField(
        verbose_name=_("Text or description"),
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name=_("Task of topic"),
        related_name="tasks",
    )

    def __str__(self) -> str:
        """String representation of object."""
        return f"Task {self.type_task}, title {self.title}"

    class Meta:
        verbose_name_plural = _("Tasks")
        verbose_name = _("Task")


class Answer(BaseModel):
    """Model for Question."""

    is_true = models.BooleanField(
        verbose_name=_("Is true answer"),
        default=False,
    )
    content = models.TextField(
        verbose_name=_("Content of answer"),
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_("Task of answers"),
        related_name="answers",
    )

    def __str__(self) -> str:
        """String representation of object."""
        return f"Answer {self.content}, is_true {self.is_true}"

    class Meta:
        verbose_name_plural = _("Answers")
        verbose_name = _("Answer")


class Comment(BaseModel):
    """Model for Comment."""

    content = models.TextField(
        verbose_name=_("Content of comment"),
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_("Task of comment"),
        related_name="comments",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Parent comment"),
        related_name="child_comments",
        default=None,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET(get_sentinel_user),
        verbose_name=_("Owner of comment"),
    )

    def __str__(self) -> str:
        """String representation of object."""
        return f"Comment {self.content}"

    class Meta:
        verbose_name_plural = _("Comments")
        verbose_name = _("Comment")
