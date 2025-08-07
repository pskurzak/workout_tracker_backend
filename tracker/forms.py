from django import forms
from .models import WorkoutLog

class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ['exercise', 'date', 'sets', 'reps', 'weight']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
