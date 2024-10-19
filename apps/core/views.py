from django.http import JsonResponse


def ping(request):
    if request.method == "GET":
        return JsonResponse({"ping": "pong"})

    return JsonResponse({"error": "Method Not Allowd"}, status=405)
