from django.db import migrations
from django.contrib.auth.models import User


def create_superuser(apps, schema_editor):
    if not User.objects.exists():
        User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')


class Migration(migrations.Migration):

    dependencies = [
        ("transaction", "0001_initial"),
    ]

    operations = [

        migrations.RunPython(create_superuser),
    ]
