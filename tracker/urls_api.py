from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import (
    ExerciseListView,
    WorkoutLogViewSet,
    WorkoutSessionViewSet,
    SignupView,
    ProfileView
)

router = DefaultRouter()
router.register(r'exercises', ExerciseListView, basename='exercise')
router.register(r'workouts', WorkoutLogViewSet, basename='workoutlog')
router.register(r'sessions', WorkoutSessionViewSet, basename='workoutsession')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
