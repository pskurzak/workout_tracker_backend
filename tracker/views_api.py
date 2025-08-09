from rest_framework import generics, viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from .models import Exercise, WorkoutLog
from .serializers import ExerciseSerializer, WorkoutLogSerializer

from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# /api/exercises/
class ExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]  # keep consistent with workouts API


# /api/workouts/ (list, create, retrieve, update, delete)
class WorkoutLogViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return only the current user's logs in a stable order so the client
        can group by session_id and keep sets in creation order.
        """
        return (
            WorkoutLog.objects
            .filter(user=self.request.user)
            .order_by('date', 'session_id', 'id')  # stable ascending
        )

    def perform_create(self, serializer):
        # Attach the current authenticated user to the workout log.
        # session_id comes from the client (optional); model default will fill it if missing.
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this workout.")
        instance.delete()


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
