# backend/initiatives/forms.py
from django import forms
from .models import Initiative

class InitiativeForm(forms.ModelForm):
    class Meta:
        model = Initiative
        fields = ['title', 'description', 'initiator_name', 'email', 'image']
