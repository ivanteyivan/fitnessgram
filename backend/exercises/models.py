from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Exercise(models.Model):
    name = models.CharField(
        verbose_name="Название упражнения",
        max_length=128,
        unique=True,
        db_index=True,
    )
    muscle_group = models.CharField(
        verbose_name="Группа мышц",
        max_length=128,
    )
    description = models.TextField(
        verbose_name="Описание упражнения",
        blank=True,
    )
    difficulty = models.CharField(
        verbose_name="Сложность",
        max_length=20,
        choices=[
            ('beginner', 'Начинающий'),
            ('intermediate', 'Средний'),
            ('advanced', 'Продвинутый'),
        ],
        default='beginner'
    )

    class Meta:
        verbose_name = "Упражнение"
        verbose_name_plural = "Упражнения"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.muscle_group})"
