from rest_framework import generics, viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Exercise, WorkoutLog, WorkoutSession
from .serializers import (
    ExerciseSerializer,
    WorkoutLogSerializer,
    WorkoutSessionSerializer,
)

# /api/exercises/
class ExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]


# /api/workouts/
class WorkoutLogViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            WorkoutLog.objects
            .filter(user=self.request.user)
            .select_related("exercise", "session")
            .order_by("-date", "-id")
        )

    def perform_create(self, serializer):
        # user enforced in serializer
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this workout.")
        instance.delete()


# /api/sessions/
class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = WorkoutSession.objects.filter(user=self.request.user)
        include = self.request.query_params.get("include_entries")
        if include == "1":
            # serializer already includes entries; prefetch for perf
            qs = qs.prefetch_related("entries__exercise")
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # name updates
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("Invalid session.")
        serializer.save()


# /api/signup/
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("username")
    email = request.data.get("email", "")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password)
    except ValidationError as e:
        return Response({"error": list(e)}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "Account created successfully"}, status=status.HTTP_201_CREATED)


# /api/me/
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })
