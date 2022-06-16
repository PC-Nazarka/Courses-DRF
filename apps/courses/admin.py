from django.contrib import admin

from . import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    """Class representation of Course model in admin panel."""

    autocomplete_fields = (
        "students",
        "category",
    )
    search_fields = ("name",)
    list_display = (
        "id",
        "name",
        "description",
        "image",
        "price",
        "created",
        "modified",
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Class representation of Category model in admin panel."""

    search_fields = ("name",)
    list_display = (
        "id",
        "name",
        "created",
        "modified",
    )


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    """Class representation of Topic model in admin panel."""

    autocomplete_fields = ("course",)
    search_fields = ("title",)
    list_display = (
        "id",
        "title",
        "number",
        "created",
        "modified",
    )


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    """Class representation of Task model in admin panel."""

    search_fields = ("title",)
    list_display = (
        "id",
        "type_task",
        "title",
        "text",
        "created",
        "modified",
    )


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Class representation of Answer model in admin panel."""

    autocomplete_fields = ("task",)
    search_fields = ("content",)
    list_display = (
        "id",
        "is_true",
        "content",
        "created",
        "modified",
    )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    """Class representation of Comment model in admin panel."""

    autocomplete_fields = (
        "task",
        "parent",
        "user",
    )
    search_fields = ("content",)
    list_display = (
        "id",
        "content",
        "created",
        "modified",
    )


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """Class representation of Review model in admin panel."""

    autocomplete_fields = (
        "user",
        "course",
    )
    list_display = (
        "id",
        "rating",
        "review",
        "created",
        "modified",
    )
