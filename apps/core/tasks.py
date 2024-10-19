from celery import shared_task


@shared_task
def test_task():
    """
    This task can be executed periodically using Celery Beat, and/or on demand.

    To call this task on demand:
        1.- Start a Celery worker with the following command:
            $ celery -A conf worker -l info
        2.- Call the task from a View or another function: test_task.delay()'

    To set the periodic task:
        1.- Go the Django Admin and add a new Periodic Task.
        2.- Make sure to have a running instance of a Celery worker:
            $ celery -A conf worker -l info
        3.- Start Celery Beat with following command:
            $ celery -A conf beat -l INFO
    """
    print("Hello World from Celery")
