from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from order.models import Order, OrderItem
from restaurant.models import Unit
from menu.models import Item
from order.forms import CartNameForm

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
    orders = Order.objects.filter(user__id=request.user.id).exclude(status='CR')
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
        if cart_name == '': cart_name = request.user.username
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
def send(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    current_order = __get_current_order(request, unit)
    if request.method == 'POST':
        if unit.minimum_ord_val > current_order.total_amount:
            return render_to_response('order/minimum_val_fail.html', {
                                  'order': current_order,
                                  }, context_instance=RequestContext(request))
        current_order.status = 'ST'
        current_order.save()
        return render_to_response('order/send_complete.html', {
                                  'order': current_order,
                                  }, context_instance=RequestContext(request))
    else:
        return render_to_response('order/send_confirmation.html', {
                                  'order': current_order,
                                  }, context_instance=RequestContext(request))


def add_cart(request, unit_id):
  unit = get_object_or_404(Unit, pk=unit_id)
  if request.method == 'POST':
      form = CartNameForm(request.POST)
      if form.is_valid(): # All validation rules pass
          next_cart = request.POST['name']
          return render_to_response('order/order_cart.html', {
                                  'cartname': next_cart,
                                  'object': unit,
                                  }, context_instance=RequestContext(request))
  else:
      form = CartNameForm() # An unbound form
  return render_to_response('order/cart_name.html', {
        'form': form,
        'object': unit,
    }, context_instance=RequestContext(request))



@login_required
def get_total_amount(request, order_id):
  order = get_object_or_404(Order, pk=order_id)
  return HttpResponse(str(order.total_amount))

@login_required
def get_subtotal(request, unit_id, cart_name):
  unit = get_object_or_404(Unit, pk=unit_id)
  current_order = __get_current_order(request, unit)
  return HttpResponse(str(current_order.get_cart_subtotal(cart_name)))
