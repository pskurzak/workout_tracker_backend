"""
URL configuration for workout_tracker project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),

    # Privacy Policy page (served by Django TemplateView)
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),

    # DRF API (your iOS app uses these)
    path('api/', include('tracker.urls_api')),

    # Token login endpoint for the iOS app
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Optional placeholder HTML views (your existing tracker.urls)
    path('', include('tracker.urls')),
]
