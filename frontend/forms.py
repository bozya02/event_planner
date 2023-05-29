from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.utils import timezone

from core.models import *


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'last_name', 'first_name', 'password1', 'password2']


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'photo']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs.update({'class': 'form-control datetimepicker'})


class NewEmployeeForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'groups']


class EmployeeForm(UserChangeForm):
    password = None
    password_changed = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'groups', 'password', 'password_changed']


