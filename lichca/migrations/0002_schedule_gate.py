from django.db import migrations


def create_gate(apps, schema_editor):
    gate = apps.get_model("lichca", "ScheduleGate")
    gate.objects.using(schema_editor.connection.alias).get_or_create(id=1)


def remove_gate(apps, schema_editor):
    gate = apps.get_model("lichca", "ScheduleGate")
    gate.objects.using(schema_editor.connection.alias).filter(id=1).delete()


class Migration(migrations.Migration):
    dependencies = [("lichca", "0001_initial")]
    operations = [migrations.RunPython(create_gate, remove_gate)]
