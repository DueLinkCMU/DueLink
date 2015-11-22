__author__ = 'pimengfu'
from django import template

register = template.Library()


@register.filter(name='iso8061')
def addslashes_doublequote(value):
    return value
