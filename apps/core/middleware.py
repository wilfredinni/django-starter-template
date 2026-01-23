import logging
import time
import uuid
from contextvars import ContextVar

# ContextVars to replace threading.local for async safety
request_id_var = ContextVar("request_id", default="none")
client_ip_var = ContextVar("client_ip", default="")
user_id_var = ContextVar("user_id", default="anonymous")
path_var = ContextVar("path", default="")
response_time_var = ContextVar("response_time", default=0.0)
status_code_var = ContextVar("status_code", default=0)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = (
        x_forwarded_for.split(",")[0].strip()
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR", "")
    )
    return ip


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.id = request_id

        request_id_var.set(request_id)
        client_ip_var.set(get_client_ip(request))
        path_var.set(request.path)

        if hasattr(request, "user") and request.user.is_authenticated:
            user_id_var.set(str(getattr(request.user, "id", "anonymous")))
        else:
            user_id_var.set("anonymous")

        start_time = time.time()

        try:
            response = self.get_response(request)

            response_time = time.time() - start_time
            response_time_var.set(response_time)
            status_code_var.set(response.status_code)

            response["X-Request-ID"] = request_id
            response["X-Response-Time"] = f"{response_time:.3f}s"

            return response

        except Exception:
            response_time = time.time() - start_time
            response_time_var.set(response_time)
            status_code_var.set(500)
            raise


class TimeLogFilter(logging.Filter):
    """
    Filter to ensure we only log records that have a response_time.
    Useful for access logs, but DANGEROUS for error logs.
    """

    def filter(self, record):
        return response_time_var.get() != 0.0


class RequestIDFilter(logging.Filter):
    """
    Injects context variables into the log record.
    """

    def filter(self, record):
        record.request_id = request_id_var.get()
        record.client = client_ip_var.get()
        record.path = path_var.get()
        record.user_id = user_id_var.get()
        record.response_time = response_time_var.get()
        record.status_code = status_code_var.get()
        return True
