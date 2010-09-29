from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.exceptions import PermissionDenied 
from order.models import Order, OrderItem
from restaurant.models import Unit
from menu.models import Item
from order.forms import CartNameForm, OrderForm

def __get_current_order(request, unit):
    try:
        co = Order.objects.filter(status='CR').get(unit__id=unit.id)
        if co.is_abandoned():
            raise
    except:
        unit = Unit.objects.get(pk=unit.id)
        co = Order.objects.create(user=request.user, unit=unit)
    return co

def __is_restaurant_administrator(request, unit):
    if not unit.admin_users: raise PermissionDenied()
    admin_user_list = [u.strip() for u in unit.admin_users.split(",")]
    if request.user.username not in admin_user_list:
        raise PermissionDenied()

@login_required
def list(request):
    orders = Order.objects.filter(user__id=request.user.id).exclude(status='CR')
    return render_to_response('order/order_list.html', {
                                  'order_list': orders,
                                  }, context_instance=RequestContext(request))

@login_required
def list_unit(request, unit_id):
    orders = Order.objects.filter(user__id=request.user.id).filter(unit=unit_id).exclude(status='CR')
    return render_to_response('order/order_list_div.html', {
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
        form = OrderForm(request.POST, instance=current_order)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = 'ST'
            order.save()
            messages.add_message(request, messages.WARNING, _('Your order has been sent to the restaurant!'))
            return redirect('order:timer', unit_id=unit.id)
    else:
        form = OrderForm(instance=current_order)
    return render_to_response('order/send_confirmation.html', {
                                  'form': form,                                 
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
  
@login_required
def timer(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    return render_to_response('order/timer.html', {
                                  'unit': unit,
                                  }, context_instance=RequestContext(request))

@login_required
def clone(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    current_order = __get_current_order(request, order.unit)
    current_order.delete()
    new_order = order.clone()
    if new_order.total_amount != order.total_amount:
        messages.add_message(request, messages.WARNING, _('The price of some items has changed. Please review the order!'))
    return redirect('restaurant:restaurant_detail', object_id=order.unit_id)

@login_required
def restlist(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    __is_restaurant_administrator(request, unit)
    orders = Order.objects.filter(unit=unit_id).filter(status__in=['ST', 'RV'])
    return render_to_response('order/restaurant_order_list.html', {
                                  'order_list': orders,
                                  'unit_id': unit_id,
                                  }, context_instance=RequestContext(request))

@login_required
def restlist_ajax(request, unit_id):
    orders = Order.objects.filter(unit=unit_id).filter(status__in=['ST', 'RV'])
    return render_to_response('order/restaurant_order_list_div.html', {
                                  'order_list': orders,
                                  }, context_instance=RequestContext(request))

@login_required
def restdetail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.status == 'ST':
        order.status = u'RV'
        order.save()
    return render_to_response('order/restaurant_order_detail.html', {
                                  'order': order,
                                  }, context_instance=RequestContext(request))

@login_required
def mark_delivered(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = u'DL'
    order.save()
    return HttpResponse(order.get_status_display())
