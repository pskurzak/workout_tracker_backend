from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Exercise, WorkoutLog
from .serializers import ExerciseSerializer, WorkoutLogSerializer


class DefaultPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 500


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all().order_by("name")
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkoutLogViewSet(viewsets.ModelViewSet):
    """
    Flat CRUD for workout rows (each set/entry).
    The iOS app groups by session_id on the client.
    """
    serializer_class = WorkoutLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        # Return only current user's rows, newest first
        return (
            WorkoutLog.objects
            .filter(user=self.request.user)
            .select_related("exercise")
            .order_by("-date", "-id")
        )

    def perform_create(self, serializer):
        """
        ✅ Minimal fix:
        - Respect client-provided session_id so multiple rows belong to the same workout.
        - Don’t overwrite it on the server.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def my_exercises(self, request):
        """
        Optional helper endpoint returning distinct free‑text exercise names user has used.
        (Your iOS 'ExerciseSearchView' can query this.)
        """
        q = request.query_params.get("q", "").strip().lower()
        names = (
            WorkoutLog.objects.filter(user=request.user)
            .exclude(exercise_name__isnull=True)
            .exclude(exercise_name__exact="")
            .values_list("exercise_name", flat=True)
            .distinct()
        )
        if q:
            names = [n for n in names if q in n.lower()]
        return Response([{"name": n} for n in names])
