from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
from exercises.views import ExerciseViewSet
from workout_plans.views import WorkoutPlanViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('exercises', ExerciseViewSet)
router.register('workout-plans', WorkoutPlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
