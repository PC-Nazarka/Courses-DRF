from apps.courses import factories

COURSES_COUNT = 5
TOPIC_COUNT = 5
TASK_COUNT = 5
ANSWER_COUNT = 5
COMMENT_COUNT = 5
REVIEW_COUNT = 5


def run():
    """Generate examples of Courses, ."""
    courses = factories.CourseFactory.create_batch(size=COURSES_COUNT)
    for course in courses:
        topics = factories.TopicFactory.create_batch(
            size=TOPIC_COUNT,
            course=course,
        )
        for topic in topics:
            tasks = factories.TaskFactory.create_batch(
                size=TASK_COUNT,
                topic=topic,
            )
            for task in tasks:
                factories.AnswerFactory.create_batch(
                    size=ANSWER_COUNT,
                    task=task,
                )
                factories.CommentFactory.create_batch(
                    size=COMMENT_COUNT,
                    task=task,
                )
        factories.ReviewFactory.create_batch(
            size=REVIEW_COUNT,
            course=course,
        )
