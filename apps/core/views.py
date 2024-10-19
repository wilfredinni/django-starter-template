from django.http import JsonResponse

from .tasks import test_task


def ping(request):
    if request.method == "GET":
        return JsonResponse({"ping": "pong"})

    return JsonResponse({"error": "Method Not Allow"}, status=405)


def fire_task(request):
    if request.method == "GET":
        test_task.delay()
        return JsonResponse({"task": "Task fired"})

    return JsonResponse({"error": "Method Not Allow"}, status=405)
