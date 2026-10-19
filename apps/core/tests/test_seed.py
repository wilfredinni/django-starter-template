from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import override_settings
from rest_framework.test import APITestCase

from apps.users.models import CustomUser


class SeedTests(APITestCase):
    @override_settings(DEBUG=False)
    def test_production_seed_is_blocked_before_cleaning(self):
        user = CustomUser.objects.create_user("keep@example.com", "safe-password")
        with self.assertRaisesMessage(CommandError, "DEBUG"):
            call_command("seed", users=1, clean=True, stdout=StringIO())
        self.assertTrue(CustomUser.objects.filter(pk=user.pk).exists())

    @override_settings(DEBUG=True)
    def test_seed_creates_sample_users_without_known_passwords_or_admin(self):
        output = StringIO()
        call_command("seed", users=2, stdout=output)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertFalse(CustomUser.objects.filter(is_superuser=True).exists())
        for user in CustomUser.objects.all():
            self.assertTrue(user.has_usable_password())
            self.assertFalse(user.check_password("testpass123"))
            self.assertFalse(user.check_password("admin"))
            self.assertNotIn(user.password, output.getvalue())
