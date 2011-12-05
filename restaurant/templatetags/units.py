from django import template
from restaurant.models import Unit
from datetime import date

register = template.Library()

@register.simple_tag(takes_context=True)
def random_units(context):
    units = Unit.objects.filter(active=True).order_by('?')
    context['random_units'] = units
    return ''
