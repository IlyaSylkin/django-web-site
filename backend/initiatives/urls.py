from . import views
from django.urls import path
from .views import review_initiatives

urlpatterns = [
    path('create/', views.initiatives_create, name='initiatives_create'),
    path('<int:pk>', views.InitiativesDetailView.as_view() ,name='initiative-detail'),
    path('review', review_initiatives, name='review_initiatives'),
    path('approve/<int:id>/', views.approve_initiative, name='approve_initiative'),
    path('reject/<int:id>/', views.reject_initiative, name='reject_initiative'),
    path('vote/<int:id>/', views.vote_initiative, name='vote_initiative'),
    path('initiatives/<int:pk>/', views.InitiativesDetailView.as_view(), name='initiative-detail'),
    path('initiatives/<int:initiative_id>/comment/', views.add_comment, name='add_comment'),
]
