from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Exercise
from .serializers import ExerciseSerializer, ExerciseShortSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ExerciseShortSerializer
        return ExerciseSerializer
