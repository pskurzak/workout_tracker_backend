from django import forms
from .models import WorkoutLog, Exercise


class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        # ✅ Removed "date" because it's auto_now_add and non-editable
        fields = [
            "exercise",
            "sets",
            "reps",
            "weight",
            "session_ref",
            "client_session_id",
            "user",
        ]


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["name", "category"]
