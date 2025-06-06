from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from users.models import Follow
from users.serializers import (
    UserSerializer,
    UserWithWorkoutPlansSerializer,
    FollowSerializer,
)
from workout_plans.models import WorkoutPlan, Favorite
from workout_plans.serializers import WorkoutPlanSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ("username", "email")
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return UserWithWorkoutPlansSerializer
        return UserSerializer

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == "POST":
            if user == author:
                return Response(
                    {"error": "Нельзя подписаться на самого себя!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {"error": "Вы уже подписаны на этого пользователя!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(author, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            if not Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {"error": "Вы не подписаны на этого пользователя!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Follow.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        if not Follow.objects.filter(user=user).exists():
            return Response(
                {"error": "Вы ни на кого не подписаны."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follows = Follow.objects.filter(user=user)
        authors = [follow.author for follow in follows]
        serializer = FollowSerializer(authors, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[
        IsAuthenticated])
    def me(self, request):
        """Возвращает информацию о текущем пользователе."""
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get", "put", "patch", "delete"],
        permission_classes=[IsAuthenticated],
        url_path="me/avatar",
    )
    def avatar(self, request):
        """Управляет аватаром пользователя.

        GET - возвращает текущий аватар
        PUT/PATCH - обновляет аватар
        DELETE - удаляет аватар
        """
        user = request.user
        if request.method == "GET":
            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data)

        if request.method in ["PUT", "PATCH"]:
            if "avatar" not in request.data:
                return Response(
                    {"errors": ERRORS["no_image"]}, status=status.
                    HTTP_400_BAD_REQUEST
                )
            serializer = AddAvatar(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "DELETE":
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"error": "Метод не разрешен"}, status=status.
            HTTP_405_METHOD_NOT_ALLOWED
        )
