from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from .models import Exercise, WorkoutLog, WorkoutSession
from .serializers import (
    ExerciseSerializer, WorkoutLogSerializer, WorkoutSessionSerializer,
    SignupSerializer, UserSerializer
)


# ----- Pagination -----
class DefaultPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 500


# ----- Exercises -----
class ExerciseListView(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.AllowAny]


# ----- Workout Logs -----
class WorkoutLogViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        return WorkoutLog.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ----- Workout Sessions -----
class WorkoutSessionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]


# ----- Signup -----
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data["username"])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


# ----- Profile -----
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ----- My Exercises -----
class MyExercisesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = (request.query_params.get("q") or "").strip().lower()

        fk_names = WorkoutLog.objects.filter(
            user=request.user, exercise__isnull=False
        ).values_list("exercise__name", flat=True)

        free_names = WorkoutLog.objects.filter(
            user=request.user
        ).exclude(exercise_name="").values_list("exercise_name", flat=True)

        names = {n for n in fk_names if n} | {n for n in free_names if n}

        if q:
            names = {n for n in names if q in n.lower()}

        recent = list(
            WorkoutLog.objects.filter(user=request.user)
            .exclude(exercise_name="")
            .order_by("-id")
            .values_list("exercise_name", flat=True)
        )
        order = {name: i for i, name in enumerate(recent)}
        sorted_names = sorted(names, key=lambda n: order.get(n, 10**9))

        return Response([{"name": n} for n in sorted_names[:50]])


# ----- Account Deletion -----
class AccountDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
