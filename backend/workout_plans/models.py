from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from exercises.models import Exercise

User = get_user_model()


class WorkoutPlan(models.Model):
    name = models.CharField(
        verbose_name="Название плана тренировок",
        max_length=128,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        related_name="workout_plans",
        verbose_name="Автор плана",
        on_delete=models.CASCADE,
        db_index=True,
    )
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        verbose_name="Фотография",
        upload_to="workout_plans_photo/",
    )
    exercises = models.ManyToManyField(
        Exercise,
        verbose_name="Упражнения",
        through="WorkoutPlanExercise",
        related_name="workout_plans",
        blank=False,
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name="Длительность (минуты)",
        validators=[
            MinValueValidator(
                1,
                message="Длительность не может быть меньше 1 минуты",
            ),
        ],
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "План тренировок"
        verbose_name_plural = "Планы тренировок"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class WorkoutPlanExercise(models.Model):
    workout_plan = models.ForeignKey(
        WorkoutPlan,
        verbose_name="План тренировок",
        on_delete=models.CASCADE,
        related_name="exercises_items",
    )
    exercise = models.ForeignKey(
        Exercise,
        verbose_name="Упражнение",
        on_delete=models.CASCADE,
    )
    sets = models.PositiveSmallIntegerField(
        verbose_name="Количество подходов",
        validators=[MinValueValidator(
            1,
            message="Количество подходов не может быть менее 1")],
    )
    reps = models.PositiveSmallIntegerField(
        verbose_name="Количество повторений",
        validators=[MinValueValidator(
            1,
            message="Количество повторений не может быть менее 1")],
    )

    class Meta:
        verbose_name = "Упражнение в плане"
        verbose_name_plural = "Упражнения в планах"

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    workout_plan = models.ForeignKey(
        WorkoutPlan, 
        verbose_name="План тренировок",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "workout_plan"],
                name="unique_user_workout_plan_in_favorites"
            )
        ]

    def __str__(self):
        return f"{self.user} {self.workout_plan}"


class WorkoutPlanShortLink(models.Model):
    workout_plan = models.ForeignKey(
        WorkoutPlan, 
        verbose_name="План тренировок", 
        on_delete=models.CASCADE
    )
    url_hash = models.CharField(
        verbose_name="Хэш", 
        max_length=10, 
        unique=True, 
        db_index=True
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания ссылки", 
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Короткая ссылка на план тренировок"
        verbose_name_plural = "Короткие ссылки на планы тренировок"

    def __str__(self):
        return f"{self.url_hash} -> {self.workout_plan.name}"
