from django import template

register = template.Library()

@register.tag
def get_cart_subtotal(parser, token):
    return SubtotalNode()

class SubtotalNode(template.Node):
    def render(self, context):
        if context.has_key('order') and context.has_key('cartname'): 
            order = context['order']
            cart = context['cartname']
            return order.get_cart_subtotal(cart)
        return '0'