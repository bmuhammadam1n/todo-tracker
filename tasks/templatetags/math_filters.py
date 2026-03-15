# tasks/templatetags/math_filters.py
from django import template

register = template.Library()

@register.filter
def minus(value, arg):
    """Subtract arg from value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value