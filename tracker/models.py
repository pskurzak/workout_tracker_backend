from django.db import models
from django.contrib.auth.models import User
import uuid

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_sessions")
    name = models.CharField(max_length=100, default="Workout")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField()
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField(null=True, blank=True)

    # OLD client-side grouping id (kept for backward compatibility)
    client_session_id = models.CharField(max_length=36, default=lambda: str(uuid.uuid4()), db_index=True)

        # inside class WorkoutLog(models.Model):
    session_ref = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="entries",
        db_index=True,
    )


    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        w = f" {self.weight}kg" if self.weight is not None else ""
        return f"{self.exercise.name} {self.sets}x{self.reps}{w}"
