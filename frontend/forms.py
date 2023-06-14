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

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'last_name', 'first_name', 'password1', 'password2']

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description']

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(label='Дата начала', initial=timezone.now() + timezone.timedelta(days=1),
                                     widget=DateTimePickerInput(options={'format': 'DD.MM.YYYY HH:mm'}),
                                     input_formats=DATETIME_INPUT_FORMATS)

    end_date = forms.DateTimeField(label='Дата окончания', initial=timezone.now() + timezone.timedelta(days=1),
                                   widget=DateTimePickerInput(options={'format': 'DD.MM.YYYY HH:mm'}),
                                   input_formats=DATETIME_INPUT_FORMATS)

    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'start_date', 'end_date', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['start_date'].widget.attrs.update({'class': 'form-control datetimepicker'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control datetimepicker'})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and start_date < timezone.now():
            self.add_error('start_date', 'Дата начала должна быть не ранее текущего времени.')

        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', 'Дата окончания должна быть не ранее даты начала.')

        return cleaned_data


class NewEmployeeForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'groups']

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EmployeeForm(UserChangeForm):
    password = None
    password_changed = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'groups', 'password', 'password_changed']

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NewEventTaskForm(forms.ModelForm):
    start_date = forms.DateTimeField(label='Дата начала',
                                     widget=DateTimePickerInput(options={'format': 'DD.MM.YYYY HH:mm'}),
                                     input_formats=DATETIME_INPUT_FORMATS)
    plan_end_date = forms.DateTimeField(label='Планируемая дата окончания',
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
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['event_user'].queryset = EventUser.objects.filter(event=event)
        self.fields['event_user'].label_from_instance = self.format_event_user_label

        if event:
            self.fields['start_date'].initial = event.start_date + timezone.timedelta(minutes=1)
            self.fields['plan_end_date'].initial = event.end_date - timezone.timedelta(minutes=1)

        self.fields['start_date'].widget.attrs.update({'class': 'form-control datetimepicker'})
        self.fields['plan_end_date'].widget.attrs.update({'class': 'form-control datetimepicker'})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        plan_end_date = cleaned_data.get('plan_end_date')
        event = cleaned_data.get('event_user').event

        if event:
            print(start_date)
            print(start_date)
            print(start_date < event.start_date)
            if start_date and start_date < event.start_date:
                self.add_error('start_date', 'Дата начала не может быть раньше даты начала мероприятия.')

            if plan_end_date and (plan_end_date > event.end_date):
                self.add_error('plan_end_date',
                               'Плановая дата окончания не может быть позже даты окончания мероприятия.')
            if start_date and plan_end_date and start_date > plan_end_date:
                self.add_error('plan_end_date',
                               'Плановая дата окончания не может быть позже даты окончания мероприятия.')
        return cleaned_data


class EventTaskStateForm(forms.ModelForm):
    class Meta:
        model = EventTask
        fields = ['state']

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
