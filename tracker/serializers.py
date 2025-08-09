# tracker/serializers.py
from rest_framework import serializers
from .models import Exercise, WorkoutLog

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'category']


class WorkoutLogSerializer(serializers.ModelSerializer):
    # Read: nested exercise object
    exercise = ExerciseSerializer(read_only=True)
    # Write: exercise_id -> exercise FK
    exercise_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercise.objects.all(),
        source='exercise',
        write_only=True
    )
    # Allow client to send a session_id; if omitted, model default generates one
    session_id = serializers.UUIDField(required=False)

    class Meta:
        model = WorkoutLog
        fields = [
            'id',
            'exercise', 'exercise_id',
            'date', 'sets', 'reps', 'weight',
            'user',
            'session_id',
        ]
        read_only_fields = ['id', 'user']

    def validate_sets(self, v):
        if v <= 0:
            raise serializers.ValidationError("Sets must be > 0.")
        return v

    def validate_reps(self, v):
        if v <= 0:
            raise serializers.ValidationError("Reps must be > 0.")
        return v
