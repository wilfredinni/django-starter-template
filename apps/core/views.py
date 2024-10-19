from django.http import JsonResponse

from .tasks import test_task


def ping(request):
    """
    Handles a ping request to check if the server is responsive.
    """
    if request.method == "GET":
        return JsonResponse({"ping": "pong"})

    return JsonResponse({"error": "Method Not Allow"}, status=405)


def fire_task(request):
    """
    Handles a request to fire a test Celery task. The task will be retried
    up to 3 times and after 5 seconds if it fails (by default). The retry
    time will be increased exponentially.
    """
    if request.method == "GET":
        test_task.delay()
        return JsonResponse({"task": "Task fired"})

    return JsonResponse({"error": "Method Not Allow"}, status=405)
