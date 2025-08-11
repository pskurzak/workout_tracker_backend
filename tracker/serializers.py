from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Exercise, WorkoutLog, WorkoutSession


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = [
            "id", "user",
            "exercise", "exercise_name",
            "date", "sets", "reps", "weight",
            "session_id", "session_ref",
            "name",
        ]
        read_only_fields = ["user", "session_id"]

    def validate(self, attrs):
        # allow PATCH: get current instance values as fallback
        exercise = attrs.get("exercise", getattr(self.instance, "exercise", None))
        exercise_name = attrs.get("exercise_name", getattr(self.instance, "exercise_name", ""))

        if not exercise and not (exercise_name and exercise_name.strip()):
            raise serializers.ValidationError("Provide exercise_name (free text) or exercise id.")

        if exercise_name:
            attrs["exercise_name"] = " ".join(exercise_name.split())[:100]
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = ["id", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
