from django import template

register = template.Library()

@register.tag
def get_cart_subtotal(parser, token):
    return SubtotalNode()

class SubtotalNode(template.Node):
    def render(self, context):
        order = context['order']
        cart = context['cart']
        return order.get_cart_subtotal(cart)