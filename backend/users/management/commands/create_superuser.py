from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser with default credentials'

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@example.com").exists():
            User.objects.create_superuser(
                email="admin@example.com",
                password="admin",
                username="admin",
                first_name="Админ",
                last_name="Админ",
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created superuser')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Superuser already exists')
            ) 