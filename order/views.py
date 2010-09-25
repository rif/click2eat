from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from order.models import Order, OrderItem
from restaurant.models import Unit
from menu.models import Item

def __get_current_order(request, unit):
    try:
        co = Order.objects.filter(status='CR').get(unit__id=unit.id)
        if co.is_abandoned():
            raise
    except:
        unit = Unit.objects.get(pk=unit.id)
        co = Order.objects.create(user=request.user, unit=unit)
    return co

@login_required
def list(request):
    orders = Order.objects.filter(user__id=request.user.id)
    return render_to_response('order/order_list.html', {
                                  'order_list': orders,
                                  }, context_instance=RequestContext(request))

"""@login_required
def create(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    order = Order.objects.create(user=request.user, unit=unit)
    return HttpResponse(str(order))"""

@login_required
def add_item(request, item_id, cart_name):
    item = get_object_or_404(Item, pk=item_id)
    try:
        current_order = __get_current_order(request, item.unit)
        order_item = OrderItem.objects.create(order=current_order, item=item, cart=cart_name)
        return HttpResponse(str(order_item.id))
    except:
        raise Http404()

@login_required
def remove_item(request, item_id):
    item = get_object_or_404(OrderItem, pk=item_id)
    item.delete()
    return HttpResponse('ok')

@login_required
def get_current_order(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    return render_to_response('order/order_div.html', {
                                  'order': __get_current_order(request, unit),
                                  }, context_instance=RequestContext(request))

@login_required
def add_cart(request, unit_id):
  unit = get_object_or_404(Unit, pk=unit_id)
  current_order = __get_current_order(request, unit)
  carts = current_order.orderitem_set.values_list('cart', flat=True)
  carts = [cart for cart in carts if cart != None]
  next_cart = _("cart") + str(len(carts))
  return render_to_response('order/order_cart.html', {
                                  'cartname': next_cart,
                                  'object': unit,
                                  }, context_instance=RequestContext(request))

@login_required
def get_total_amount(request, unit_id):
  unit = get_object_or_404(Unit, pk=unit_id)
  current_order = __get_current_order(request, unit)
  return HttpResponse(str(current_order.total_amount))