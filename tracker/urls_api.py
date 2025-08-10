from django.urls import path
from rest_framework.routers import DefaultRouter
from .views_api import (
    ExerciseListView,
    WorkoutLogViewSet,
    WorkoutSessionViewSet,
    signup,
    me,
)

router = DefaultRouter()
router.register(r'workouts', WorkoutLogViewSet, basename='workout')
router.register(r'sessions', WorkoutSessionViewSet, basename='session')

urlpatterns = [
    path("exercises/", ExerciseListView.as_view(), name="exercise-list"),
    path("signup/", signup, name="signup"),
    path("me/", me, name="me"),
]

urlpatterns += router.urls