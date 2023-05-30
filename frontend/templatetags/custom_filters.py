import datetime

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
    else:
        return 'bg-secondary'


@register.filter
def tasks_count(event_tasks, state):
    return len(event_tasks.filter(state=state))
