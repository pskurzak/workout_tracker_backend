import uuid
from django.db import models
from django.contrib.auth.models import User


# ✅ Add this so older migrations still work
def generate_uuid():
    return str(uuid.uuid4())


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkoutSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - {self.created_at}"


class WorkoutLog(models.Model):
    date = models.DateField()
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4)
    session_ref = models.ForeignKey(
        WorkoutSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100, default="Workout")

    # If you still want to keep user tracking:
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"
