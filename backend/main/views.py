from django.shortcuts import render
from initiatives.models import Initiative



def about(request):
    return render(request, 'main/about.html')
def index(request):
    if request.path == '/winners/':
        initiatives = Initiative.objects.filter(status='winner').order_by('-submission_date')
    # Получаем все инициативы со статусом 'approved' и сортируем их по дате отправки
    else:
        initiatives = Initiative.objects.filter(status='approved').order_by('-submission_date')
    
    # Рендерим шаблон home.html и передаем переменные
    return render(request, 'main/main.html', {'initiatives': initiatives})
