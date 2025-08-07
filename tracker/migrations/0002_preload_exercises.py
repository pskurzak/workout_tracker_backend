from django.db import migrations

def add_exercises(apps, schema_editor):
    Exercise = apps.get_model('tracker', 'Exercise')
    preset_exercises = [
        ("Push-up", "Chest"),
        ("Pull-up", "Back"),
        ("Squat", "Legs"),
        ("Deadlift", "Legs"),
        ("Bench Press", "Chest"),
        ("Bicep Curl", "Biceps"),
        ("Overhead Press", "Shoulders"),
        ("Plank", "Core"),
        ("Russian Twist", "Core"),
        ("Face Pull", "Shoulders"),
        ("Overhead Tricep Extension", "Triceps"),
        ("RDL", "Legs"),
        ("Bulgarian Split Squat", "Legs"),
        ("Lateral Raise", "Shoulders"),
    ]
    for name, category in preset_exercises:
        Exercise.objects.create(name=name, category=category)

def remove_exercises(apps, schema_editor):
    Exercise = apps.get_model('tracker', 'Exercise')
    Exercise.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_exercises, remove_exercises),
    ]
