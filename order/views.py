from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from order.models import Order
from restaurant.models import Unit


@login_required
def list(request):
    orders = Order.objects.filter(user__id=request.user.id)
    return render_to_response('order/order_list.html', {
                                  'order_list': orders,
                                  }, context_instance=RequestContext(request))
    
def create(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    order = Order.objects.create(user=request.user, unit=unit)
    return HttpResponse('OK')
