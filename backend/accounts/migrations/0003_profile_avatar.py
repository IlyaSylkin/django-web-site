# Generated by Django 5.1.2 on 2024-11-02 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_profile_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                default="avatars/default_avatar.png", upload_to="avatars/"
            ),
        ),
    ]