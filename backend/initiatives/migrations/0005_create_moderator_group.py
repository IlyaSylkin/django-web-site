from django.db import migrations
from django.contrib.auth.models import Group

def create_moderator_group(apps, schema_editor):
    Group.objects.get_or_create(name='Moderators')

class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0001_initial'),  # Замените на номер вашей начальной миграции
    ]

    operations = [
        migrations.RunPython(create_moderator_group),
    ]
