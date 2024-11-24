from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
        ('winner', 'Победитель'),
        ('inactive', 'Неактивно'),
    ]

class Initiative(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiatives')
    title = models.CharField(max_length=200, verbose_name="Краткое описание инициативы")
    description = models.TextField(verbose_name="Детальное описание инициативы")
    initiator_name = models.CharField(max_length=100, verbose_name="Имя инициатора")
    email = models.EmailField(verbose_name="Электронная почта")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    votes = models.IntegerField(default=0, verbose_name="Количество голосов")
    voted_users = models.ManyToManyField(User, related_name='voted_initiatives', blank=True)
    moderator_comment = models.TextField(blank=True, null=True, default='нет', verbose_name="Комментарий модератора")
    winner_month = models.CharField(max_length=20, blank=True, null=True, verbose_name="Победивший месяц")

    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Инициатива"
        verbose_name_plural = "Инициативы"

class InitiativeImage(models.Model):
    initiative = models.ForeignKey(Initiative, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='initiatives/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.initiative.title}"

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

class Update(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, related_name='updates')
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class UpdateImage(models.Model):
    update = models.ForeignKey(Update, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='updates/')
    