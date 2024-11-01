# Generated by Django 5.1.2 on 2024-10-28 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Initiative",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=200, verbose_name="Название инициативы"
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание инициативы")),
                (
                    "initiator_name",
                    models.CharField(max_length=100, verbose_name="Имя инициатора"),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="Электронная почта"),
                ),
                (
                    "submission_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата отправки"
                    ),
                ),
            ],
        ),
    ]
