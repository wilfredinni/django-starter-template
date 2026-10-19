from secrets import token_urlsafe

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction

from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Seed database with sample data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users", default=10, type=int, help="The number of fake users to create"
        )
        parser.add_argument(
            "--clean", action="store_true", help="Delete all data before seeding"
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Seeding is only available when DEBUG=True.")

        if options["clean"]:
            self.stdout.write("Deleting old data...")
            CustomUser.objects.filter(is_superuser=False).delete()

        self.create_users(options["users"])

        self.stdout.write(self.style.SUCCESS("Successfully seeded database"))

    @transaction.atomic
    def create_users(self, count):
        try:
            from faker import Faker
        except ImportError:
            self.stdout.write(
                self.style.ERROR(
                    "Faker is not installed. Please install it to seed users."
                )
            )
            return

        fake = Faker()
        self.stdout.write(f"Creating {count} users...")

        for _ in range(count):
            sid = transaction.savepoint()
            try:
                user = CustomUser.objects.create_user(
                    email=fake.email(),
                    password=token_urlsafe(32),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                )
                transaction.savepoint_commit(sid)
                self.stdout.write(f"Created user - {user.email}")
            except IntegrityError as e:
                transaction.savepoint_rollback(sid)
                self.stdout.write(self.style.WARNING(f"Error creating user - {e}"))
