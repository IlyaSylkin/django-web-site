# accounts/urls.py
from django.urls import path
from .import views
from .views import profile_edit,UserProfileView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', views.register, name='register'),  # Представление для регистрации
    path('login/', views.UserLoginView.as_view(), name='login'),  # Класс представления для входа
    path('profile/', UserProfileView.as_view(), name='profile'),  # Путь для текущего пользователя
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),  # Путь для других пользователей
]
