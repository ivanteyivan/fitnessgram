from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from exercises.serializers import ExerciseSerializer, ExerciseShortSerializer
from .models import (
    WorkoutPlan,
    WorkoutPlanExercise,
    Favorite,
    WorkoutPlanShortLink,
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
        source='exercises_items',
        many=True,
        read_only=True,
    )
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = WorkoutPlan
        fields = (
            'id',
            'name',
            'author',
            'description',
            'image',
            'exercises',
            'duration',
            'created_at',
        )
        read_only_fields = ('id', 'author', 'created_at')


class WorkoutPlanCreateSerializer(serializers.ModelSerializer):
    exercises = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
    )

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