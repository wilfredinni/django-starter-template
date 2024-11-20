from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view

from .tasks import test_task


@extend_schema(
    description="Handles a ping request to check if the server is responsive.",
    responses={
        200: {
            "type": "object",
            "properties": {"ping": {"type": "string"}},
            "example": {"ping": "pong"},
        },
        405: {
            "type": "object",
            "properties": {"detail": {"type": "string"}},
            "example": {"detail": 'Method "POST" not allowed.'},
        },
    },
)
@api_view(["GET"])
def ping(request):
    return JsonResponse({"ping": "pong"})


def fire_task(request):
    """
    TODO 🚫 After testing the view, remove it with the task and the route.

    Handles a request to fire a test Celery task. The task will be retried
    up to 3 times and after 5 seconds if it fails (by default). The retry
    time will be increased exponentially.
    """
    if request.method == "GET":
        test_task.delay()
        return JsonResponse({"task": "Task fired"})

    return JsonResponse({"error": "Method Not Allowed"}, status=405)
