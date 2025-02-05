from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Init user data"

    def handle(self, *args, **options):
        user = get_user_model().objects.create_user(
            phone_number="1234567890", password="password"
        )

        self.stdout.write(
            self.style.SUCCESS(f"User {user.phone_number} created successfully")
        )
