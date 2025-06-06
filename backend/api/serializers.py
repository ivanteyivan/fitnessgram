from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import User
from workout_plans.serializers import WorkoutPlanSerializer
from djoser.serializers import UserCreateSerializer, UserSerializer


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
        )
        return user


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserWithWorkoutPlansSerializer(UserSerializer):
    workout_plans = serializers.SerializerMethodField()
    workout_plans_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'workout_plans',
            'workout_plans_count',
        )

    def get_workout_plans(self, obj):
        request = self.context.get('request')
        workout_plans = obj.workout_plans.all()
        workout_plans_limit = request.query_params.get('workout_plans_limit')
        if workout_plans_limit and workout_plans_limit.isdigit():
            workout_plans = workout_plans[:int(workout_plans_limit)]
        return WorkoutPlanSerializer(
            workout_plans, many=True, context=self.context
        ).data

    def get_workout_plans_count(self, obj):
        return obj.workout_plans.count()
