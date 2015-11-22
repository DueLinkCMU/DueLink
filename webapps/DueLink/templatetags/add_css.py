from django import template

register = template.Library()


@register.filter(name='add_css')
def add_css(field, cls):
    return field.as_widget(
        attrs={"class": cls, "id": field.name, "placeholder": field.label})
