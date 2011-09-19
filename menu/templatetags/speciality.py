from django import template
from menu.models import Item
from datetime import date

register = template.Library()

@register.simple_tag(takes_context=True)
def random_special(context):
    item = Item.objects.filter(speciality=True).select_related('item_group__unit').order_by('?')[0]
    context['special_item'] = item
    context['today'] = date.today()
    return ''
