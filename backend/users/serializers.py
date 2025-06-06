from rest_framework import serializers
from django.contrib.auth import get_user_model
from workout_plans.models import (
    WorkoutPlan,
    Favorite,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj).exists()


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
            'is_subscribed',
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
