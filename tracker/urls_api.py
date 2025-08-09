# tracker/urls_api.py

from django.urls import path
from .views_api import ExerciseListView, WorkoutLogListCreateView, signup

urlpatterns = [
    path('exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('workouts/', WorkoutLogListCreateView.as_view(), name='workout-log-list-create'),
    path("signup/", signup, name="signup"),
]
