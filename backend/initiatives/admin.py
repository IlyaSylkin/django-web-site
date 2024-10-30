from django.contrib import admin
from .models import Initiative

@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "initiator_name",
        "submission_date",
        "votes",
    )  # Укажите поля, которые хотите отобразить
