from django import template
register = template.Library()
@register.filter()
def is_numberic(value):
    return value.isdigit()