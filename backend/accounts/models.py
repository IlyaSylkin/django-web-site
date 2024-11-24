from django.db import models
from django.contrib.auth.models import User
from initiatives.views import is_moderator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    course = models.CharField(max_length=10, blank=True, null=True)
    institute_number = models.CharField(max_length=10, blank=True, null=True)
    group = models.CharField(max_length=10, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=30, choices=[
        ('user', 'Обычный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ], default='user')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_role_display(self):
        # Проверка, является ли пользователь модератором
        if is_moderator(self.user):
            return "Модератор"
        # Вернуть роль пользователя или "не указано", если роль не определена
        return dict(self._meta.get_field('role').choices).get(self.role, "не указано")