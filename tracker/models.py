from django.db import models
from django.contrib.auth.models import User
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkoutSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="New Workout")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class WorkoutLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_ref = models.ForeignKey(
        WorkoutSession, on_delete=models.CASCADE, related_name="entries", null=True, blank=True
    )
    client_session_id = models.CharField(
        max_length=36,
        default=generate_uuid  # ✅ replaced lambda with named function
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps} ({self.user.username})"
