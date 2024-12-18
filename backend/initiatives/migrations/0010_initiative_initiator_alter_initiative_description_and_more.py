# Generated by Django 5.1.2 on 2024-11-04 13:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0009_initiative_voted_users"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="initiative",
            name="initiator",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="initiatives",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="initiative",
            name="description",
            field=models.TextField(verbose_name="Детальное описание инициативы"),
        ),
        migrations.AlterField(
            model_name="initiative",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="initiatives/",
                verbose_name="Место, которое вы хотите изменить",
            ),
        ),
        migrations.AlterField(
            model_name="initiative",
            name="title",
            field=models.CharField(
                max_length=200, verbose_name="Краткое описание инициативы"
            ),
        ),
    ]
