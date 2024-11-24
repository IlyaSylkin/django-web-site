from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class UserEditForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False)
    course = forms.CharField(max_length=10, required=False)
    institute_number = forms.CharField(max_length=10, required=False)
    group = forms.CharField(max_length=10, required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'course', 'institute_number', 'group', 'about', 'avatar']
        