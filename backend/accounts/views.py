from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm
from django.urls import reverse_lazy

# Представление для регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Представление для входа
from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'accounts/login.html'
    def get_success_url(self):
        return reverse_lazy('home')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})