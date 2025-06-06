import json
import os

from django.core.management.base import BaseCommand

from exercises.models import Exercise


class Command(BaseCommand):
    help = 'Load exercises from JSON file'

    def handle(self, *args, **options):
        with open(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "data",
                "exercises.json"
            ),
            encoding="utf-8",
        ) as file:
            data = json.load(file)
            for item in data:
                Exercise.objects.get_or_create(
                    name=item['name'],
                    defaults={
                        'muscle_group': item['muscle_group'],
                        'description': item['description'],
                        'difficulty': item['difficulty']
                    }
                )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded {len(data)} exercises')
            ) 