from django.contrib.auth.decorators import login_required, user_passes_test
#from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.db.models import Sum
from annoying.decorators import render_to
from datetime import date
from restaurant.models import Unit
from order.models import Order
from order import views

def __user_has_profile(user):
    if not user.is_authenticated(): return None
    try:
        user.get_profile()
        return None
    except:
        return redirect('profiles_create_profile')

def index(request):
    units = Unit.objects.order_by('?')
    user = request.user
    has_profile = __user_has_profile(user)
    if has_profile != None: return has_profile
    if not user.is_authenticated() or user.get_profile().is_filled():
        return render_to_response('restaurant/index.html', {
                                  'units': units,
                                  'gold': units.filter(package__slug='gold'),
                                  'platinum': units.filter(package__slug='platinum'),
                                  }, context_instance=RequestContext(request))
    else:
        return redirect('profiles_create_profile')

@login_required
@render_to('restaurant/unit_detail.html')
def unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    current_order = views.__get_current_order(request, unit)
    return {'object': unit, 'order': current_order, 'carts': current_order.get_carts()}

@render_to('restaurant/platinum_restaurant_list.html')
def get_random_platinum(request):
    units = Unit.objects.order_by('?')
    return {'platinum': units.filter(package__slug='platinum')}

@render_to('restaurant/gold_restaurant_list.html')
def get_random_gold(request):
    units = Unit.objects.order_by('?')
    return {'gold': units.filter(package__slug='gold')}

@login_required
@render_to('restaurant/package_history.html')
def package_history(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    return {'platinum': units.filter(package__slug='platinum')}


@user_passes_test(lambda u: u.is_authenticated() and u.is_staff)
@render_to('restaurant/invoice.html')
def invoice(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    today = date.today()
    start = date(today.year, today.month - 1, 1)
    end = date(today.year, today.month - 1, 30)
    last_month_orders = Order.objects.filter(unit=unit).filter(creation_date__range=(start, end)).filter(status__in=['ST', 'RV', 'DL'])
    total_amount_sum = last_month_orders.aggregate(Sum('total_amount'))['total_amount__sum']
    if total_amount_sum != None:
        grand_total = (total_amount_sum * unit.package.rate/100) + unit.package.monthly_fee
    else:
        grand_total = unit.package.monthly_fee
    return {'unit': unit, 'orders': last_month_orders, 'total_sum': total_amount_sum, 'grand_total': grand_total}
