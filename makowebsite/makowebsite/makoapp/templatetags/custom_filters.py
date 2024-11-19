# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={'class': css_class})
    return value

@register.filter
def add_class(field, css_class):
    """Add a CSS class to a form field."""
    return field.as_widget(attrs={"class": css_class})