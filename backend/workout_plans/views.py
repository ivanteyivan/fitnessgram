from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import WorkoutPlan, Favorite, WorkoutPlanShortLink
from .serializers import (
    WorkoutPlanSerializer,
    WorkoutPlanCreateSerializer,
    FavoriteSerializer,
    WorkoutPlanShortLinkSerializer,
)
from .filters import WorkoutPlanFilter


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = WorkoutPlanFilter
    search_fields = ('name', 'description', 'exercises__name')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return WorkoutPlanCreateSerializer
        return WorkoutPlanSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        workout_plan = get_object_or_404(WorkoutPlan, pk=pk)
        
        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': request.user.id, 'workout_plan': workout_plan.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        favorite = get_object_or_404(
            Favorite,
            user=request.user,
            workout_plan=workout_plan
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def create_short_link(self, request, pk=None):
        workout_plan = get_object_or_404(WorkoutPlan, pk=pk)
        serializer = WorkoutPlanShortLinkSerializer(
            data={'workout_plan': workout_plan.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
