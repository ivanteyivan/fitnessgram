import json
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from workout_plans.models import WorkoutPlan

User = get_user_model()


class Command(BaseCommand):
    help = 'Load workout plans from JSON file'

    def handle(self, *args, **options):
        # Get or create a superuser for the workout plans
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()

        with open(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "data",
                "workout_plans.json"
            ),
            encoding="utf-8",
        ) as file:
            data = json.load(file)
            for item in data:
                WorkoutPlan.objects.get_or_create(
                    name=item['name'],
                    defaults={
                        'description': item['description'],
                        'duration': item['duration'],
                        'author': admin_user
                    }
                )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded {len(data)} workout plans')
            ) 