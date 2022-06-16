from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from . import models, tasks

STUDENTS_COUNT = (100, 1000)


@receiver(m2m_changed, sender=models.Course.students.through)
def check_count_students(instance, action, pk_set, **kwargs):
    """Signal when student add to course."""
    if action == "post_add":
        if instance.students.count() in STUDENTS_COUNT:
            tasks.send_email_about_course.delay(
                "attendance",
                instance.owner.id,
                instance.id,
            )
        tasks.send_email_about_course.delay(
            "entered",
            list(pk_set)[0],
            instance.id,
        )


@receiver(post_save, sender=models.Course)
def check_status_of_course(instance, created, update_fields, **kwargs):
    """Signal when course save for send email if it has ``ready`` status."""
    is_ready_status = instance.status == models.Course.Status.READY
    updated = "status" in update_fields if update_fields else False
    if is_ready_status and (created or updated):
        tasks.send_email_about_course.delay(
            "create",
            instance.owner.id,
            instance.id,
        )


@receiver(post_delete, sender=models.Course)
def delete_img_of_course_after_delete(instance, **kwargs):
    """Signal when course has deleted."""
    instance.image.storage.delete(instance.image.path)
