from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_cart_total(context):
    if 'oc' in context and 'cn' in context: 
        oc, cn = context['oc'], context['cn']
        return oc.get_total_sum(cn)
    return '0'

@register.filter
def clean_cn(value):    
    return value.split(':')[1] if ':' in value else value