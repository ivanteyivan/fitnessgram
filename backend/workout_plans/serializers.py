import secrets
import string

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (
    WorkoutPlan,
    WorkoutPlanExercise,
    Favorite,
    WorkoutPlanShortLink,
)

User = get_user_model()


class ExerciseInputSerializer(serializers.Serializer):
    """Валидатор для одного упражнения в плане тренировок."""
    id = serializers.IntegerField(required=True, min_value=1)
    sets = serializers.IntegerField(required=True, min_value=1)
    reps = serializers.IntegerField(required=True, min_value=1)


class ExercisesWriteField(serializers.ListField):
    """Multipart: exercises приходит строкой JSON."""

    def __init__(self, **kwargs):
        kwargs['child'] = ExerciseInputSerializer()
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if isinstance(data, (str, bytes)):
            import json

            try:
                data = json.loads(data)
            except (json.JSONDecodeError, TypeError) as exc:
                raise serializers.ValidationError(
                    "Поле exercises должно быть JSON-массивом объектов "
                    '{"id", "sets", "reps"}.'
                ) from exc
        if not isinstance(data, list):
            raise serializers.ValidationError("exercises должен быть списком.")
        return super().to_internal_value(data)


class WorkoutPlanAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
        )


class WorkoutPlanExerciseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='exercise.id')
    name = serializers.ReadOnlyField(source='exercise.name')
    muscle_group = serializers.ReadOnlyField(source='exercise.muscle_group')
    difficulty = serializers.ReadOnlyField(source='exercise.difficulty')

    class Meta:
        model = WorkoutPlanExercise
        fields = ('id', 'name', 'muscle_group', 'difficulty', 'sets', 'reps')


class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutPlanExerciseSerializer(
        source="exercises_items",
        many=True,
        read_only=True,
    )
    author = WorkoutPlanAuthorSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutPlan
        fields = (
            "id",
            "name",
            "author",
            "description",
            "image",
            "exercises",
            "duration",
            "created_at",
            "is_favorited",
        )
        read_only_fields = ("id", "author", "created_at", "is_favorited")

    def get_is_favorited(self, obj):
        return bool(getattr(obj, "is_favorited_flag", False))


class WorkoutPlanCreateSerializer(serializers.ModelSerializer):
    exercises = ExercisesWriteField(write_only=True)

    class Meta:
        model = WorkoutPlan
        fields = (
            'id',
            'name',
            'description',
            'image',
            'exercises',
            'duration',
        )

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        workout_plan = WorkoutPlan.objects.create(**validated_data)
        
        for exercise_data in exercises_data:
            WorkoutPlanExercise.objects.create(
                workout_plan=workout_plan,
                exercise_id=exercise_data['id'],
                sets=exercise_data['sets'],
                reps=exercise_data['reps'],
            )
        
        return workout_plan

    def update(self, instance, validated_data):
        if 'exercises' in validated_data:
            exercises_data = validated_data.pop('exercises')
            instance.exercises_items.all().delete()
            
            for exercise_data in exercises_data:
                WorkoutPlanExercise.objects.create(
                    workout_plan=instance,
                    exercise_id=exercise_data['id'],
                    sets=exercise_data['sets'],
                    reps=exercise_data['reps'],
                )
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'workout_plan')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'workout_plan'],
                message='Этот план тренировок уже в избранном'
            )
        ]


class WorkoutPlanShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlanShortLink
        fields = ('url_hash', 'workout_plan', 'created_at')
        read_only_fields = ('url_hash', 'created_at')

    def create(self, validated_data):
        alphabet = string.ascii_lowercase + string.digits
        for _ in range(50):
            url_hash = ''.join(secrets.choice(alphabet) for _ in range(10))
            if not WorkoutPlanShortLink.objects.filter(url_hash=url_hash).exists():
                return WorkoutPlanShortLink.objects.create(
                    url_hash=url_hash, **validated_data
                )
        raise serializers.ValidationError(
            {'url_hash': ['Не удалось сгенерировать уникальный хэш.']}
        )