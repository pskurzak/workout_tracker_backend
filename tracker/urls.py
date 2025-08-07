from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_workout, name='log_workout'),
    path('logs/', views.view_logs, name='view_logs'),  # placeholder for later
]
