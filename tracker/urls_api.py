# tracker/urls_api.py
from rest_framework.routers import DefaultRouter
from .views_api import ExerciseViewSet, WorkoutLogViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'workouts', WorkoutLogViewSet, basename='workout')

urlpatterns = router.urls
