import logging
from types import SimpleNamespace

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from apps.core.middleware import RequestIDFilter, RequestIDMiddleware, get_client_ip


class RequestContextTests(SimpleTestCase):
    def log_context(self):
        record = logging.makeLogRecord({})
        RequestIDFilter().filter(record)
        return {
            field: getattr(record, field)
            for field in (
                "request_id",
                "client",
                "path",
                "user_id",
                "response_time",
                "status_code",
            )
        }

    def test_context_is_restored_after_success_and_exception(self):
        initial = self.log_context()
        seen = []

        def respond(request):
            seen.append(self.log_context())
            if request.path == "/error/":
                raise ValueError("request failed")
            return HttpResponse()

        middleware = RequestIDMiddleware(respond)
        request = RequestFactory().get("/first/", REMOTE_ADDR="192.0.2.1")
        request.user = SimpleNamespace(is_authenticated=True, pk=42)
        response = middleware(request)
        self.assertEqual(response["X-Request-ID"], seen[0]["request_id"])
        self.assertEqual(seen[0]["client"], "192.0.2.1")
        self.assertEqual(seen[0]["user_id"], "42")
        self.assertEqual(self.log_context(), initial)

        with self.assertRaisesMessage(ValueError, "request failed"):
            middleware(RequestFactory().get("/error/"))
        self.assertEqual(seen[1]["user_id"], "anonymous")
        self.assertEqual(seen[1]["response_time"], 0.0)
        self.assertEqual(seen[1]["status_code"], 0)
        self.assertEqual(self.log_context(), initial)

    def test_forwarded_ip_is_not_trusted(self):
        request = RequestFactory().get(
            "/", REMOTE_ADDR="192.0.2.1", HTTP_X_FORWARDED_FOR="203.0.113.1"
        )
        self.assertEqual(get_client_ip(request), "192.0.2.1")

    def test_invalid_peer_ip_is_not_logged(self):
        request = RequestFactory().get("/", REMOTE_ADDR="invalid\r\nforged log")
        self.assertEqual(get_client_ip(request), "")
