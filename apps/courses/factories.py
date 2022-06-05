import factory
from factory import fuzzy

from apps.users.factories import UserFactory

from . import models


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Category instance."""

    name = factory.Faker(
        "month_name",
    )

    class Meta:
        model = models.Category
        django_get_or_create = ("name",)


class CourseFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Course instanse."""

    name = factory.Faker(
        "currency_name",
    )
    description = factory.Faker(
        "catch_phrase",
    )
    image = factory.django.ImageField(
        color="green",
    )
    price = factory.Faker(
        "pydecimal",
        left_digits=9,
        right_digits=2,
        positive=True,
        min_value=1.0,
    )
    category = factory.SubFactory(
        CategoryFactory,
    )

    class Meta:
        model = models.Course


class TopicFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Topic instanse."""

    title = factory.Faker(
        "currency_name",
    )
    number = factory.Faker(
        "pyint",
    )
    course = factory.SubFactory(
        CourseFactory,
    )

    class Meta:
        model = models.Topic


class TaskFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Task instanse."""

    type_task = fuzzy.FuzzyChoice([item[0] for item in models.Task.Type.choices])
    title = factory.Faker(
        "currency_name",
    )
    text = factory.Faker(
        "catch_phrase",
    )
    topic = factory.SubFactory(
        TopicFactory,
    )

    class Meta:
        model = models.Task


class AnswerFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Answer instanse."""

    is_true = factory.Faker(
        "pybool",
    )
    content = factory.Faker(
        "catch_phrase",
    )
    task = factory.SubFactory(
        TaskFactory,
    )

    class Meta:
        model = models.Answer


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Comment instanse."""

    content = factory.Faker(
        "catch_phrase",
    )
    task = factory.SubFactory(
        TaskFactory,
    )
    user = factory.SubFactory(
        UserFactory,
    )

    class Meta:
        model = models.Comment


class ReviewFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Review instanse."""

    rating = factory.Faker(
        "pyint",
        min_value=1,
        max_value=5,
    )
    review = factory.Faker(
        "catch_phrase",
    )
    user = factory.SubFactory(
        UserFactory,
    )
    course = factory.SubFactory(
        CourseFactory,
    )

    class Meta:
        model = models.Review
