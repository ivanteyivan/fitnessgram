import json
import django
import os
from exercises.models import Exercise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodgram.settings")
django.setup()


def load_exercises():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "exercises.json"
        ),
        encoding="utf-8",
    ) as file:
        data = json.load(file)
    for item in data:
            Exercise.objects.create(**item)
        print(f"Успешно загружено {len(data)} упражнений")


if __name__ == "__main__":
    load_exercises()
