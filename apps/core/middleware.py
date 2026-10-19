import logging
import time
import uuid
from contextvars import ContextVar
from ipaddress import ip_address

# ContextVars to replace threading.local for async safety
request_id_var = ContextVar("request_id", default="none")
client_ip_var = ContextVar("client_ip", default="")
user_id_var = ContextVar("user_id", default="anonymous")
path_var = ContextVar("path", default="")
response_time_var = ContextVar("response_time", default=0.0)
status_code_var = ContextVar("status_code", default=0)


def get_client_ip(request):
    try:
        return str(ip_address(request.META.get("REMOTE_ADDR", "")))
    except ValueError:
        return ""


class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        request.id = request_id

        if hasattr(request, "user") and request.user.is_authenticated:
            user_id = str(getattr(request.user, "pk", "anonymous"))
        else:
            user_id = "anonymous"

        tokens = [
            (variable, variable.set(value))
            for variable, value in (
                (request_id_var, request_id),
                (client_ip_var, get_client_ip(request)),
                (path_var, request.path),
                (user_id_var, user_id),
                (response_time_var, 0.0),
                (status_code_var, 0),
            )
        ]

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
        finally:
            for variable, token in reversed(tokens):
                variable.reset(token)


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
