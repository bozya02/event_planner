import datetime

import django.utils.timezone
from django import template

register = template.Library()


@register.filter
def add_class(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})


@register.filter
def set_hidden(field):
    return field.as_widget(attrs={'type': 'hidden'})


@register.filter
def add_onchange(field, onchange):
    return field.as_widget(attrs={'class': field.field.widget.attrs.get('class'), 'onchange': onchange})


@register.filter
def is_future(value):
    return value.date() > datetime.date.today()


@register.filter
def get_state_color(state_name):
    if state_name == 'Выполнена':
        return 'bg-success'
    elif state_name == 'В процессе':
        return 'bg-info'
    elif state_name == 'Новая':
        return 'bg-warning'
    elif state_name == 'Не выполнена':
        return 'bg-danger'
    elif state_name == 'Повтор':
        return 'bg-secondary'
    else:
        return 'bg-secondary'


@register.filter
def tasks_count(event_tasks, state):
    return len(event_tasks.filter(state=state))


@register.filter
def get_employee_status(employee):
    if employee.eventtask_set.filter(state__name='Выполнена').count() == employee.eventtask_set.count():
        return 'Свободен'
    else:
        return 'Занят'


@register.filter
def is_event_actual(event):
    return django.utils.timezone.now() < event.start_date


@register.filter
def can_edit_task(task):
    return task.state.name != 'Выполнена' and task.state.name != "Не выполнена"


@register.filter
def is_director(user):
    return 'Директор' in user.groups.values_list('name', flat=True)
