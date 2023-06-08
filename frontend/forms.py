from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.utils import timezone

from core.models import *
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


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
    start_date = forms.DateField(label='Дата начала', initial=timezone.now(),
                                 widget=DateTimePickerInput())

    end_date = forms.DateField(label='Дата окончания', initial=timezone.now(),
                               widget=DateTimePickerInput())

    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'start_date', 'end_date', 'photo']
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
        fields = ['first_name', 'last_name', 'email', 'username', 'groups', 'password', 'password_changed']


class NewEventTaskForm(forms.ModelForm):
    start_date = forms.DateField(label='Дата начала', initial=timezone.now(), widget=DateTimePickerInput())
    plan_end_date = forms.DateField(label='Планируемая дата окончания', initial=timezone.now(),
                                    widget=DateTimePickerInput())

    class Meta:
        model = EventTask
        fields = ['name', 'description', 'event_user', 'photo', 'start_date', 'plan_end_date']
