import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exercises.models import Exercise
from workout_plans.models import WorkoutPlan, WorkoutPlanExercise

User = get_user_model()


class Command(BaseCommand):
    help = 'Load test data from JSON files'

    def handle(self, *args, **options):
        # Создаем суперпользователя, если его нет
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin'
            )
            self.stdout.write(self.style.SUCCESS('Created superuser'))

        # Загружаем упражнения
        exercises_file = os.path.join('data', 'exercises.json')
        if not os.path.exists(exercises_file):
            self.stdout.write(self.style.ERROR(f'File not found: {exercises_file}'))
            return

        with open(exercises_file, 'r', encoding='utf-8') as f:
            exercises_data = json.load(f)

        for exercise_data in exercises_data:
            Exercise.objects.get_or_create(
                name=exercise_data['name'],
                defaults={
                    'muscle_group': exercise_data['muscle_group'],
                    'description': exercise_data['description'],
                    'difficulty': exercise_data['difficulty']
                }
            )
        self.stdout.write(self.style.SUCCESS('Loaded exercises'))

        # Загружаем планы тренировок
        workout_plans_file = os.path.join('data', 'workout_plans.json')
        if not os.path.exists(workout_plans_file):
            self.stdout.write(self.style.ERROR(f'File not found: {workout_plans_file}'))
            return

        with open(workout_plans_file, 'r', encoding='utf-8') as f:
            workout_plans_data = json.load(f)

        admin_user = User.objects.get(username='admin')
        for plan_data in workout_plans_data:
            plan, created = WorkoutPlan.objects.get_or_create(
                name=plan_data['name'],
                author=admin_user,
                defaults={
                    'description': plan_data['description'],
                    'duration': plan_data['duration']
                }
            )

            # Добавляем упражнения в план
            for exercise_data in plan_data['exercises']:
                exercise = Exercise.objects.get(name=exercise_data['name'])
                WorkoutPlanExercise.objects.get_or_create(
                    workout_plan=plan,
                    exercise=exercise,
                    defaults={
                        'sets': exercise_data['sets'],
                        'reps': exercise_data['reps']
                    }
                )

        self.stdout.write(self.style.SUCCESS('Loaded workout plans')) 