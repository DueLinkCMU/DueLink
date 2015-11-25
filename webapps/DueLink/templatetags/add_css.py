from django import template

register = template.Library()


@register.filter(name='add_css')
def add_css(field, cls):
    return field.as_widget(
        attrs={"class": cls, "id": field.name, "placeholder": field.label})


@register.filter(name='add_css_id')
def add_css(field, cls):
    return field.as_widget(
        attrs={"class": cls, "id": "id_" + field.name, "placeholder": field.label})
