# Generated by Django 4.2.21 on 2025-06-05 17:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='Название плана тренировок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='workout_plans_photo/', verbose_name='Фотография')),
                ('duration', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Длительность не может быть меньше 1 минуты')], verbose_name='Длительность (минуты)')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_plans', to=settings.AUTH_USER_MODEL, verbose_name='Автор плана')),
            ],
            options={
                'verbose_name': 'План тренировок',
                'verbose_name_plural': 'Планы тренировок',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WorkoutPlanShortLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_hash', models.CharField(db_index=True, max_length=10, unique=True, verbose_name='Хэш')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания ссылки')),
                ('workout_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout_plans.workoutplan', verbose_name='План тренировок')),
            ],
            options={
                'verbose_name': 'Короткая ссылка на план тренировок',
                'verbose_name_plural': 'Короткие ссылки на планы тренировок',
            },
        ),
        migrations.CreateModel(
            name='WorkoutPlanExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sets', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество подходов не может быть менее 1')], verbose_name='Количество подходов')),
                ('reps', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество повторений не может быть менее 1')], verbose_name='Количество повторений')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercises.exercise', verbose_name='Упражнение')),
                ('workout_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises_items', to='workout_plans.workoutplan', verbose_name='План тренировок')),
            ],
            options={
                'verbose_name': 'Упражнение в плане',
                'verbose_name_plural': 'Упражнения в планах',
            },
        ),
        migrations.AddField(
            model_name='workoutplan',
            name='exercises',
            field=models.ManyToManyField(related_name='workout_plans', through='workout_plans.WorkoutPlanExercise', to='exercises.exercise', verbose_name='Упражнения'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('workout_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout_plans.workoutplan', verbose_name='План тренировок')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
            },
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'workout_plan'), name='unique_user_workout_plan_in_favorites'),
        ),
    ]
