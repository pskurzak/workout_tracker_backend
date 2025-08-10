from django.db import migrations, models
import uuid

def uuid_str():
    return str(uuid.uuid4())

class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0003_add_workout_session_and_fk"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name="workoutlog",
                    name="session_id",
                    field=models.CharField(
                        max_length=36,
                        default=uuid_str,   # safe, serializable function
                        db_index=True,
                    ),
                ),
            ],
        ),
    ]
