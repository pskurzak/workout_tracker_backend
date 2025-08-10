# tracker/serializers.py
from rest_framework import serializers
from .models import Exercise, WorkoutLog, WorkoutSession

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "name", "category"]


class WorkoutLogSerializer(serializers.ModelSerializer):
    # Read: nested exercise
    exercise = ExerciseSerializer(read_only=True)
    # Write: exercise_id
    exercise_id = serializers.PrimaryKeyRelatedField(
        source="exercise", queryset=Exercise.objects.all(), write_only=True
    )

    # NEW: allow client to send FK session id OR legacy session_id string
    session = serializers.PrimaryKeyRelatedField(
        queryset=WorkoutSession.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    session_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = WorkoutLog
        fields = [
            "id",
            "exercise", "exercise_id",
            "date", "sets", "reps", "weight",
            "user",
            # read-only echo:
            "session_id",
            # write-only FK:
            "session",
        ]
        read_only_fields = ["id", "user", "session_id"]

    def validate_sets(self, v):
        if v <= 0:
            raise serializers.ValidationError("Sets must be > 0.")
        return v

    def validate_reps(self, v):
        if v <= 0:
            raise serializers.ValidationError("Reps must be > 0.")
        return v

    def create(self, validated):
        """
        Accept either:
         - session (int) → attach to that WorkoutSession
         - or session_id (string) → leave as-is; a signal/backfill will attach it
         - or nothing → leave both null/auto; app can still work
        """
        user = self.context["request"].user

        # If session FK provided, enforce ownership
        sess = validated.pop("session", None)
        if sess is not None:
            if sess.user_id != user.id:
                raise serializers.ValidationError("Invalid session.")
            validated["session"] = sess

        validated["user"] = user
        return super().create(validated)


class WorkoutSessionEntrySerializer(serializers.ModelSerializer):
    """Used when embedding entries under a session."""
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutLog
        fields = ["id", "exercise", "date", "sets", "reps", "weight"]


class WorkoutSessionSerializer(serializers.ModelSerializer):
    entries = WorkoutSessionEntrySerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutSession
        fields = ["id", "name", "created_at", "entries"]
