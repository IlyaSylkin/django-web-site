from django.shortcuts import render, redirect, get_object_or_404
from .forms import InitiativeForm,CommentForm
from django.views.generic import DetailView
from initiatives.models import Initiative
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from initiatives.models import Initiative, Vote

def initiatives_create(request):
    error = ''
    if request.method == 'POST':
        form = InitiativeForm(request.POST, request.FILES)
        if form.is_valid():
            initiative = form.save(commit=False)  # Не сохраняем сразу
            initiative.status = 'pending'  # Устанавливаем статус на "На проверке"
            initiative.save()  # Сохраняем данные в базу

            return redirect('home')  # Перенаправление на главную страницу
        else:
            error = "Ошибка при заполнении формы."
    else:
        form = InitiativeForm()
    return render(request, "initiatives/create.html", {'form': form, 'error': error})

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
def review_initiatives(request):
    initiatives = Initiative.objects.filter(status='pending')
    return render(request, 'initiatives/review_initiatives.html', {'initiatives': initiatives})

@user_passes_test(is_moderator)
def approve_initiative(request, id):
    initiative = get_object_or_404(Initiative, id=id)
    initiative.status = 'approved'
    initiative.save()
    return redirect('review_initiatives')

@user_passes_test(is_moderator)
def reject_initiative(request, id):
    initiative = get_object_or_404(Initiative, id=id)
    initiative.status = 'rejected'
    initiative.save()
    return redirect('review_initiatives')

@login_required
def vote_initiative(request, id):
    initiative = get_object_or_404(Initiative, id=id)

    # Проверяем, проголосовал ли пользователь уже за эту инициативу
    if Vote.objects.filter(user=request.user, initiative=initiative).exists():
        return render(request, 'initiatives/details_view.html', {
            'initiative': initiative,
            'error': 'Вы уже проголосовали за эту инициативу.',
            'comments': initiative.comments.all(),  # Передаем комментарии
            'comment_form': CommentForm(),  # Передаем форму для комментариев
        })

    # Если нет, создаем новый голос
    Vote.objects.create(user=request.user, initiative=initiative)

    # Увеличиваем количество голосов в инициативе
    initiative.votes += 1
    initiative.save()

    return redirect('initiative-detail', pk=initiative.id)  # Перенаправление на страницу детали инициативы