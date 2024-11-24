from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('winners/', views.index, name='winners'),  # Путь для победителей]
]