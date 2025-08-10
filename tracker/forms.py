from django import forms
from .models import WorkoutLog

class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        exclude = ['user', 'client_session_id']  # exclude non-editable + auto fields
