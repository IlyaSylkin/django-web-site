from django.shortcuts import render, redirect, get_object_or_404
from .forms import InitiativeForm,CommentForm, InitiativeImageForm
from django.views.generic import DetailView
from initiatives.models import Initiative, Vote
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Initiative, InitiativeImage, Update, UpdateImage


@login_required
def user_initiatives(request, user_id):
    # Получаем пользователя по user_id
    user = get_object_or_404(User, id=user_id)
    # Получаем все инициативы, связанные с этим пользователем
    initiatives = Initiative.objects.filter(user=user).order_by('-submission_date')
    
    return render(request, 'initiatives/user_initiatives.html', {
        'user': user,
        'initiatives': initiatives,
    })

@login_required
def initiatives_create(request):
    error = ''
    if request.method == 'POST':
        form = InitiativeForm(request.POST, request.FILES)
        image_form = InitiativeImageForm(request.POST, request.FILES)
        if form.is_valid():
            initiative = form.save(commit=False)
            initiative.user = request.user
            initiative.initiator_name = request.user.get_full_name() or request.user.username
            initiative.email = request.user.email
            initiative.status = 'pending'
            initiative.save()

            # Сохраняем изображения
            if image_form.is_valid() and 'images' in request.FILES:
                for img in request.FILES.getlist('images'):
                    InitiativeImage.objects.create(initiative=initiative, image=img)

            return redirect('home')
        else:
            error = "Ошибка при заполнении формы."
    else:
        form = InitiativeForm()
        image_form = InitiativeImageForm()

    return render(request, "initiatives/create.html", {'form': form, 'image_form': image_form, 'error': error})
class InitiativesDetailView(DetailView):
    model = Initiative
    template_name = 'initiatives/details_view.html'
    context_object_name = 'initiative'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_moderator'] = self.request.user.groups.filter(name='Moderators').exists()
        context['comments'] = self.object.comments.all()  # Получаем все комментарии
        context['comment_form'] = CommentForm()  # Передаем форму для комментария
        return context
    
@login_required
def add_comment(request, initiative_id):
    initiative = get_object_or_404(Initiative, id=initiative_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Устанавливаем текущего пользователя как автора комментария
            comment.initiative = initiative  # Привязываем комментарий к инициативе
            comment.save()  # Сохраняем комментарий
            return redirect('initiative-detail', pk=initiative.id)  # Перенаправление на страницу детали инициативы
    return redirect('initiative-detail', pk=initiative.id)  # Если форма недействительна

def is_moderator(user):
    return user.groups.filter(name='Moderators').exists()

@user_passes_test(is_moderator)
def review_initiatives_show(request):
    initiatives = Initiative.objects.filter(status='pending')
    return render(request, 'initiatives/review_initiatives.html', {'initiatives': initiatives})

@user_passes_test(is_moderator)
@login_required
def review_initiative(request, id):
    initiative = get_object_or_404(Initiative, id=id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('comment', 'нет')  # Устанавливаем значение по умолчанию "нет"

        if action == 'approve':
            initiative.status = 'approved'
            initiative.moderator_comment = comment  # Здесь мы можем сохранить комментарий как причину одобрения, если хотите
        elif action == 'reject':
            initiative.status = 'rejected'
            initiative.moderator_comment = comment  # Сохраняем комментарий как причину отказа

        initiative.save()
        return redirect('review_initiatives')

    # В случае, если метод не POST (например, GET), просто перенаправляем на страницу проверки
    return redirect('review_initiatives')

@login_required
def vote_initiative(request, id):
    initiative = get_object_or_404(Initiative, id=id)

    # Проверяем, проголосовал ли пользователь уже за эту инициативу
    vote, created = Vote.objects.get_or_create(user=request.user, initiative=initiative)

    if created:
        # Если голос только что создан, добавляем пользователя в voted_users
        initiative.voted_users.add(request.user)
        initiative.votes += 1
        initiative.save()
    else:
        # Если голос уже существует, удаляем пользователя из voted_users
        initiative.voted_users.remove(request.user)
        vote.delete()
        initiative.votes -= 1
        initiative.save()

    # Передаем комментарии и форму комментария в контекст
    comments = initiative.comments.all()  # Получаем все комментарии к инициативе
    comment_form = CommentForm()  # Создаем форму для нового комментария

    return render(request, 'initiatives/details_view.html', {
        'initiative': initiative,
        'comments': comments,
        'comment_form': comment_form,
    }) # Перенаправление на страницу детали инициативы

@user_passes_test(is_moderator)
@login_required
def select_winner(request):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    
    # Получаем все инициативы со статусом 'approved'
    initiatives = Initiative.objects.filter(status='approved')
    
    # Сортируем инициативы по количеству голосов в убывающем порядке
    initiatives = initiatives.annotate(votes_count=Count('voted_users')).order_by('-votes_count')
    
    # Находим максимальное количество голосов
    if initiatives.exists():
        max_votes = initiatives.first().votes_count
        # Фильтруем инициативы, чтобы оставить только те, у которых максимальное количество голосов
        initiatives = initiatives.filter(votes_count=max_votes)
    else:
        initiatives = []

    if request.method == 'POST':
        winner_initiative_id = request.POST.get('winner_initiative')
        selected_month = request.POST.get('month')
        
        # Находим инициативу-победителя
        winner_initiative = Initiative.objects.get(id=winner_initiative_id)
        
        # Обновляем статус победителя и сохраняем месяц победы
        winner_initiative.status = 'winner'
        winner_initiative.winner_month = selected_month  # Сохраняем месяц победы
        winner_initiative.save()

        # Устанавливаем статус 'inactive' для остальных инициатив
        Initiative.objects.filter(status='approved').exclude(id=winner_initiative.id).update(status='inactive')
        
        return redirect('select_winner')  # Перенаправляем на страницу после выбора победителя

    return render(request, 'initiatives/select_winner.html', {
        'months': months,
        'initiatives': initiatives,
    })

@user_passes_test(is_moderator)
def add_update(request, initiative_id):
    if request.method == "POST":
        initiative = get_object_or_404(Initiative, id=initiative_id)
        description = request.POST.get('description')
        update = Update.objects.create(initiative=initiative, description=description)
        
        images = request.FILES.getlist('images')
        for image in images:
            UpdateImage.objects.create(update=update, image=image)
        
        return redirect('initiative-detail', pk=initiative.id)