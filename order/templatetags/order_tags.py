from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_cart_total(context):
    if 'oc' in context and 'cn' in context: 
        oc, cn = context['oc'], context['cn']
        return oc.get_total_sum(cn)
    return '0'

@register.simple_tag(takes_context=True)
def show_incr_link(context): 
    oc, cn, item = context['oc'], context['cn'], context['item']
    item_id = item.get_item_id()
    for item in oc.carts[cn]:
        if item_id in item.get_item_id() and item.get_item_id() != item_id:
            return ''
    return '<a class="incr-link" href="#"></a>'

@register.filter
def clean_cn(value):    
    return value.split(':')[1] if ':' in value else value