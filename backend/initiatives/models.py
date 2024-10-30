from django.db import models
from django.contrib.auth.models import User

class Initiative(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название инициативы")
    description = models.TextField(verbose_name="Описание инициативы")
    initiator_name = models.CharField(max_length=100, verbose_name="Имя инициатора")
    email = models.EmailField(verbose_name="Электронная почта")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    image = models.ImageField(upload_to='initiatives/', blank=True, null=True, verbose_name="Изображение инициативы")
    votes = models.IntegerField(default=0, verbose_name="Количество голосов")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Инициатива"
        verbose_name_plural = "Инициативы"
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'initiative')  # Ограничение на уникальность
        def __str__(self):
            return f"{self.user} голосовал за {self.initiative}"
        

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    initiative = models.ForeignKey(Initiative, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'