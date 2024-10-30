from django.shortcuts import render
from initiatives.models import Initiative

def index(request):
    # Проверяем, является ли пользователь модератором
    is_moderator = request.user.groups.filter(name='Moderators').exists() if request.user.is_authenticated else False

    # Получаем все инициативы со статусом 'approved' и сортируем их по дате отправки
    initiatives = Initiative.objects.filter(status='approved').order_by('-submission_date')
    
    # Рендерим шаблон home.html и передаем переменные
    return render(request, 'main/main.html', {'initiatives': initiatives, 'is_moderator': is_moderator})


def about(request):
    return render(request, 'main/about.html')
