from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Exercise, WorkoutLog, WorkoutSession

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class WorkoutLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutLog
        fields = '__all__'

    def create(self, validated_data):
        return WorkoutLog.objects.create(**validated_data)

class WorkoutSessionSerializer(serializers.ModelSerializer):
    logs = WorkoutLogSerializer(many=True, read_only=True, source='workoutlog_set')

    class Meta:
        model = WorkoutSession
        fields = ['id', 'user', 'started_at', 'logs']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
