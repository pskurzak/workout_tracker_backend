from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token  # ✅ Add this line


urlpatterns = [
    path('', views.log_workout, name='log_workout'),
    path('logs/', views.view_logs, name='view_logs'),  # placeholder for later
]
