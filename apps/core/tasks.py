import celery
from celery import shared_task


class BaseTaskWithRetry(celery.Task):
    """
    Automatically retry task in case of failure (up to 3 times). This class
    is intended to be used as a base class for other tasks that need to be
    retried in case of failure.

    Attributes:
        autoretry_for (tuple): The list of exceptions that should be caught and retried.
        retry_kwargs (dict): The maximum number of retries this task can have.
        retry_backoff (int): The time in seconds to wait before retrying the task.
        retry_jitter (bool): Whether to apply exponential backoff when retrying.
    """

    # The list of exceptions that should be caught and retried
    autoretry_for = (Exception, KeyError)

    # The maximum number of retries this task can have
    retry_kwargs = {"max_retries": 3}

    # The time in seconds to wait before retrying the task
    retry_backoff = 5

    # Whether to apply exponential backoff when retrying:
    # When you build a custom retry strategy for your Celery task
    # (which needs to send a request to another service), you should add
    # some randomness to the delay calculation to prevent all tasks from
    # being executed simultaneously resulting in a thundering herd.
    retry_jitter = True


@shared_task(bind=True, base=BaseTaskWithRetry)
def test_task(self) -> None:
    """
    This task can be executed periodically using Celery Beat, and/or on demand.

    Retry strategy
        This task uses the BaseTaskWithRetry class defined above, so it will be
        retried up to 3 times if it fails (by default). The task will be retried
        after 5 seconds, and the retry time will be increased exponentially.

    To call this task on demand
        1. Start a Celery worker with 'celery -A conf worker -l info'
        2. Call the task from a View or another function: test_task.delay()'

    To set the periodic task
        1. Go the Django Admin and add a new Periodic Task.
        2. Start a Celery worker with 'celery -A conf worker -l info'
        3. Start Celery Beat with 'celery -A conf beat -l INFO'
    """

    # 👇 To test the retries uncomment the following line:
    # raise KeyError("This is a test error")

    print("Hello World from Celery")
