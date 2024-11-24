# Generated by Django 5.1.2 on 2024-11-03 14:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0008_comment"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="initiative",
            name="voted_users",
            field=models.ManyToManyField(
                blank=True,
                related_name="voted_initiatives",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]