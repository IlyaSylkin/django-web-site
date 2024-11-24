from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import DetailView
from .models import Profile
from initiatives.views import is_moderator
from django.contrib.auth.views import LoginView
from django.conf import settings

class UserProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        if user_id is not None:
            return get_object_or_404(User, id=user_id)
        return self.request.user  # Возвращает текущего пользователя

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL  # Добавляем MEDIA_URL в контекст
        context['user'] = self.request.user
        # Получаем объект UserProfile для текущего пользователя
        user_profile, created = Profile.objects.get_or_create(user=self.get_object())
        # Добавляем аватар пользователя или аватар по умолчанию в контекст
        context['avatar'] = user_profile.avatar.url if user_profile.avatar else f"{settings.MEDIA_URL}avatars/default_avatar.png"
        context['user_profile'] = user_profile  # Передаем профиль в контекст
        
        return context
    
# Представление для регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Получите или создайте профиль для нового пользователя
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                print("Profile created successfully")  # Лог для проверки успешного создания профиля
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'accounts/login.html'
    def get_success_url(self):
        return reverse_lazy('home')

@login_required
def profile_edit(request):
    # Получите или создайте профиль пользователя
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Добавьте request.FILES для обработки загружаемого файла
        form = UserEditForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # Здесь можно добавить сообщение об успешном сохранении
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = UserEditForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {'form': form, 'MEDIA_URL': settings.MEDIA_URL})