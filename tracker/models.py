from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "Push-up", "Pull-up"
    category = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Chest", "Legs"

    def __str__(self):
        return self.name


class WorkoutLog(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)  
    date = models.DateField()  
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # optional

    def __str__(self):
        weight_str = f" @ {self.weight} lbs" if self.weight else ""
        return f"{self.date} - {self.exercise.name} ({self.sets}x{self.reps}{weight_str})"
