import os
import runpy
from unittest.mock import patch

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView


class SecuritySettingsTests(SimpleTestCase):
    def load_settings(self, missing=None, **env):
        values = {
            "DJANGO_SECRET_KEY": "test-settings-secret",
            "DATABASE_URL": "postgres://test:test@db/test",
            "REDIS_URL": "redis://redis:6379/1",
            "CELERY_BROKER_URL": "redis://redis:6379/0",
            **env,
        }
        values.pop(missing, None)
        with patch.dict(os.environ, values, clear=True), patch("environ.Env.read_env"):
            return runpy.run_path(str(settings.BASE_DIR / "conf/settings.py"))

    def test_production_does_not_allow_arbitrary_hosts(self):
        self.assertEqual(self.load_settings()["ALLOWED_HOSTS"], [])

    def test_development_allows_local_hosts(self):
        hosts = self.load_settings(DEBUG="True")["ALLOWED_HOSTS"]
        self.assertIn("localhost", hosts)
        self.assertIn("127.0.0.1", hosts)
        self.assertNotIn("*", hosts)

    def test_production_requires_explicit_cache_and_broker(self):
        for missing in ("REDIS_URL", "CELERY_BROKER_URL"):
            with self.subTest(missing=missing):
                with self.assertRaisesMessage(ImproperlyConfigured, missing):
                    self.load_settings(missing=missing)

    def test_default_api_view_is_throttled(self):
        class ExampleView(APIView):
            def get(self, request):
                return Response({"ok": True})

        cache.clear()
        self.addCleanup(cache.clear)
        with patch.dict(SimpleRateThrottle.THROTTLE_RATES, {"anon": "1/minute"}):
            view = ExampleView.as_view()
            factory = APIRequestFactory()
            self.assertEqual(view(factory.get("/")).status_code, 200)
            self.assertEqual(view(factory.get("/")).status_code, 429)
