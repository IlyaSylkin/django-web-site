from django.shortcuts import render
from initiatives.models import Initiative

def index(request):
    # Получаем все инициативы со статусом 'approved' и сортируем их по дате отправки
    initiatives = Initiative.objects.filter(status='approved').order_by('-submission_date')
    
    # Рендерим шаблон home.html и передаем переменные
    return render(request, 'main/main.html', {'initiatives': initiatives})


def about(request):
    return render(request, 'main/about.html')
