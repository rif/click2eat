from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, Http404
from order.models import Order, OrderItem
from restaurant.models import Unit
from menu.models import Item

def __get_current_order(request, unit):
    try:
        co = Order.objects.filter(status='CR').get(unit__id=unit.id)
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
def add_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    try:
        current_order = __get_current_order(request, item.unit)
        order_item = OrderItem.objects.create(order=current_order, item=item)
        return HttpResponse(str(order_item))
    except:
        raise Http404()