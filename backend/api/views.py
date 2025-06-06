from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from exercises.serializers import ExerciseShortSerializer
from workout_plans.models import (
    Exercise,
    WorkoutPlanShortLink,
)
from users.models import User
from users.serializers import UserSerializer


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseShortSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = Exercise.objects.all()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return User.objects.all()


def redirect_by_hash(request, url_hash):
    try:
        short_link = get_object_or_404(WorkoutPlanShortLink, url_hash=url_hash)
        workout_plan_id = short_link.workout_plan.id
        return redirect(f"{settings.BASE_URL}/api/workout-plans/{workout_plan_id}")
    except WorkoutPlanShortLink.DoesNotExist:
        return Response(
            {"error": "Ссылка не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
