# Generated by Django 5.1.2 on 2024-10-28 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0002_alter_initiative_options_initiative_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="initiative",
            name="votes",
            field=models.IntegerField(default=0, verbose_name="Количество голосов"),
        ),
    ]
