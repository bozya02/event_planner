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
