from django import template
from menu.models import Item
from datetime import date

register = template.Library()

@register.simple_tag(takes_context=True)
def get_name(context, item):
	return item.get_name(context['LANGUAGE_CODE'])

@register.simple_tag(takes_context=True)
def get_desc(context, item):
	return item.get_description(context['LANGUAGE_CODE'])	

