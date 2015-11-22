__author__ = 'pimengfu'
from django import template

register = template.Library()

@register.filter(name='addslashes_doublequote')
def addslashes_doublequote(value):
    return value.replace('"', '\\"')