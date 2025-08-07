from django.shortcuts import render, redirect
from .forms import WorkoutLogForm
from django.http import HttpResponse

def view_logs(request):
    return HttpResponse("Logs page coming soon...")


def log_workout(request):
    if request.method == 'POST':
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_logs')  # we’ll create this next
    else:
        form = WorkoutLogForm()
    return render(request, 'log_workout.html', {'form': form})
