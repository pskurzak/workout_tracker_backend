from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "Push-up", "Pull-up"
    category = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Chest", "Legs"

    def __str__(self):
        return self.name


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # NEW — link workout to the logged-in user
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)  
    date = models.DateField()  
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # optional

    def __str__(self):
        weight_str = f" @ {self.weight} lbs" if self.weight else ""
        return f"{self.user.username} - {self.date} - {self.exercise.name} ({self.sets}x{self.reps}{weight_str})"
