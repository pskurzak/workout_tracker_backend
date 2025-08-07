from django.contrib import admin
from .models import Exercise, WorkoutLog

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "category")

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ("date", "exercise", "sets", "reps", "weight")
    list_filter = ("date", "exercise")
