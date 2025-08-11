import uuid
from django.db import models
from django.contrib.auth.models import User
import uuid

# Compatibility for old migration 0006 that expects this symbol:
def generate_uuid() -> str:
    return str(uuid.uuid4())


class Exercise(models.Model):
    # kept for legacy rows / admin view, but not required for new data
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkoutSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - {self.created_at}"


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # New: allow **free text** exercise names; FK is optional for legacy/admin
    exercise = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.SET_NULL)
    exercise_name = models.CharField(max_length=100, blank=True, default="")

    date = models.DateField()
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    # One card per submission
    #session_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    session_id = models.CharField(max_length=36, default=generate_uuid, db_index=True)
    session_ref = models.ForeignKey(WorkoutSession, on_delete=models.SET_NULL, null=True, blank=True)

    # “title” for the workout card
    name = models.CharField(max_length=100, blank=True, default="Workout")

    def __str__(self):
        label = self.exercise_name or (self.exercise.name if self.exercise else "Exercise")
        return f"{label} - {self.sets}x{self.reps}"
