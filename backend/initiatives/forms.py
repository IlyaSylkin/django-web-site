# backend/initiatives/forms.py
from django import forms
from .models import Initiative
from .models import Comment

class InitiativeForm(forms.ModelForm):
    class Meta:
        model = Initiative
        fields = ['title', 'description', 'initiator_name', 'email', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']