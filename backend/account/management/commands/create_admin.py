from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create admin user once from environment variables"

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not email or not password:
            self.stdout.write(self.style.ERROR(
                " Missing DJANGO_SUPERUSER_* environment variables"
            ))
            return

        #  Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(
                f" Admin already exists: {email}"
            ))
            return

        #  Create superuser
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS(
            f" Admin user CREATED: {email}"
        ))
