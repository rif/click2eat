from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


@login_required
def list(request):
    orders = Order.objects.filter(user__id=request.user.id)
    return render_to_response('order/order_list.html', {
                                  'orders': orders,
                                  }, context_instance=RequestContext(request))
