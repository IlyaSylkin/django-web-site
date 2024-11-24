from . import views
from django.urls import path

urlpatterns = [
    path('create/', views.initiatives_create, name='initiatives_create'),
    path('<int:pk>/', views.InitiativesDetailView.as_view() ,name='initiative-detail'),
    path('review/', views.review_initiatives_show, name='review_initiatives'),
    path('vote/<int:id>/', views.vote_initiative, name='vote_initiative'),
    path('initiatives/<int:initiative_id>/comment/', views.add_comment, name='add_comment'),
    path('user_initiatives/<int:user_id>/', views.user_initiatives, name='user_initiatives'),
    path('select_winner/', views.select_winner, name='select_winner'),
    path('review_initiative/<int:id>/', views.review_initiative, name='review_initiative'),  # Добавлен маршрут для проверки инициативы
    path('initiatives/<int:initiative_id>/add_update/', views.add_update, name='add_update')

]   
