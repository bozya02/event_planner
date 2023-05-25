from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from core.models import *


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
