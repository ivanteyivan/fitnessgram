from django.contrib import admin

from .models import (
    WorkoutPlan,
    WorkoutPlanExercise,
    Favorite,
    WorkoutPlanShortLink,
)


class WorkoutPlanExerciseInline(admin.TabularInline):
    model = WorkoutPlanExercise
    extra = 1


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'duration', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('name', 'description')
    inlines = (WorkoutPlanExerciseInline,)
    ordering = ('-created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_plan')
    list_filter = ('user',)
    search_fields = ('user__username', 'workout_plan__name')


@admin.register(WorkoutPlanShortLink)
class WorkoutPlanShortLinkAdmin(admin.ModelAdmin):
    list_display = ('url_hash', 'workout_plan', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('url_hash', 'workout_plan__name')
    ordering = ('-created_at',)
