from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from djoser.serializers import SetPasswordSerializer

from exercises.serializers import ExerciseShortSerializer
from workout_plans.models import (
    Exercise,
    WorkoutPlanShortLink,
)
from users.models import User
from users.serializers import UserSerializer

from .serializers import CustomUserCreateSerializer
from foodgram.pagination import PageLimitPagination


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
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'list'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return User.objects.all()

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='me',
    )
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='set_password',
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get', 'put', 'patch', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='me/avatar',
    )
    def avatar(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)

        if request.method in ('PUT', 'PATCH'):
            upload = request.FILES.get('avatar')
            if not upload:
                return Response(
                    {'avatar': ['Файл не передан.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.avatar = upload
            user.save(update_fields=['avatar'])
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'DELETE':
            if user.avatar:
                user.avatar.delete(save=False)
            user.avatar = None
            user.save(update_fields=['avatar'])
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'detail': 'Метод не разрешён.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


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
