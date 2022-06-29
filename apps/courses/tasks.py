from apps.core.services import send_email
from apps.users.models import User
from config.celery_app import app

from .models import Course


@app.task(task_ignore_result=True)
def send_email_about_course(
    mode: str,
    user_id: int,
    course_id: int,
) -> None:
    """Send email to creator with some attendance of course."""
    send_email(
        mode,
        User.objects.get(pk=user_id),
        Course.objects.get(pk=course_id),
    )
