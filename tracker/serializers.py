# tracker/serializers.py
from rest_framework import serializers
from .models import Exercise, WorkoutLog

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class WorkoutLogSerializer(serializers.ModelSerializer):
    # Nested exercise for reads
    exercise = ExerciseSerializer(read_only=True)
    # Separate field for writes
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        source='exercise',
        write_only=True
    )

    class Meta:
        model = WorkoutLog
        fields = '__all__'
        read_only_fields = ['user']
