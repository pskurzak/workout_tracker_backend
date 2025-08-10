from django.db import migrations, connection

def backfill(apps, schema_editor):
    WorkoutSession = apps.get_model('tracker', 'WorkoutSession')

    # Pull raw rows so field name mismatches can't bite us
    with connection.cursor() as cur:
        cur.execute("""
            SELECT id, user_id, session_id
            FROM tracker_workoutlog
            WHERE session_ref_id IS NULL
        """)
        rows = cur.fetchall()  # (id, user_id, session_id)

    # Group by (user_id, session_id)
    from collections import defaultdict
    groups = defaultdict(list)
    for log_id, user_id, sess_key in rows:
        groups[(user_id, str(sess_key))].append(log_id)

    # Create one WorkoutSession per group and link the logs
    with connection.cursor() as cur:
        for (user_id, _sess_key), ids in groups.items():
            sess = WorkoutSession.objects.create(user_id=user_id, name="Workout")
            cur.execute(
                "UPDATE tracker_workoutlog SET session_ref_id = %s WHERE id = ANY(%s)",
                [sess.id, ids],
            )

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_add_user_and_session_id_to_workoutlog'),
    ]

    operations = [
        migrations.RunPython(backfill, reverse_code=noop),
    ]
