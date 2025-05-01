import logging
import uuid
from threading import local

_thread_locals = local()


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.id = str(uuid.uuid4())
        _thread_locals.request_id = request.id
        response = self.get_response(request)
        response["X-Request-ID"] = request.id
        return response


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(_thread_locals, "request_id", "none")
        return True
