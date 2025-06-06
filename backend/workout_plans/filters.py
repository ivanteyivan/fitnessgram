from django_filters import rest_framework as filters

from .models import WorkoutPlan


class WorkoutPlanFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author__id')
    exercises = filters.NumberFilter(field_name='exercises__id')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    duration = filters.NumberFilter(field_name='duration')

    class Meta:
        model = WorkoutPlan
        fields = ('author', 'exercises', 'is_favorited', 'duration')

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset 