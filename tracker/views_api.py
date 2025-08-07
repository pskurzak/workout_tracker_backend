# tracker/views_api.py

from rest_framework import generics
from .models import Exercise, WorkoutLog
from .serializers import ExerciseSerializer, WorkoutLogSerializer

# /api/exercises/
class ExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

# /api/workouts/
class WorkoutLogListCreateView(generics.ListCreateAPIView):
    queryset = WorkoutLog.objects.all()
    serializer_class = WorkoutLogSerializer
