from django import forms
from django.conf.global_settings import DATETIME_INPUT_FORMATS
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
    start_date = forms.DateTimeField(label='Дата начала', initial=timezone.now() + timezone.timedelta(days=1),
                                     widget=DateTimePickerInput(options={'format': 'DD.MM.YYYY HH:mm'}),
                                     input_formats=DATETIME_INPUT_FORMATS)

    end_date = forms.DateTimeField(label='Дата начала', initial=timezone.now() + timezone.timedelta(days=1),
                                   widget=DateTimePickerInput(options={'format': 'DD.MM.YYYY HH:mm'}),
                                   input_formats=DATETIME_INPUT_FORMATS)

    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'start_date', 'end_date', 'photo']

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
    start_date = forms.DateTimeField(label='Дата начала', initial=timezone.now(),
                                     widget=DateTimePickerInput(options={'format': 'DD.MM.YYYY HH:mm'}),
                                     input_formats=DATETIME_INPUT_FORMATS)
    plan_end_date = forms.DateTimeField(label='Дата начала', initial=timezone.now() + timezone.timedelta(days=1),
                                        widget=DateTimePickerInput(options={'format': 'DD.MM.YYYY HH:mm'}),
                                        input_formats=DATETIME_INPUT_FORMATS)

    def format_event_user_label(self, event_user):
        return f'{event_user.user.username} - {event_user.user.first_name} {event_user.user.last_name}'

    class Meta:
        model = EventTask
        fields = ['name', 'description', 'event_user', 'photo', 'start_date', 'plan_end_date']

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        super().__init__(*args, **kwargs)
        self.fields['event_user'].queryset = EventUser.objects.filter(event=event)
        self.fields['event_user'].label_from_instance = self.format_event_user_label
