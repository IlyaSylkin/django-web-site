# backend/initiatives/forms.py
from django import forms
from .models import Initiative, Comment, InitiativeImage


class InitiativeForm(forms.ModelForm):
    
    class Meta:
        model = Initiative
        fields = ['title', 'description']  # Добавьте сюда остальные поля, которые хотите отобразить в форме

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class InitiativeImageForm(forms.Form):
    images = forms.FileField(required=False) 