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
from django.db.models import Sum, Avg, Count
from annoying.decorators import render_to
from datetime import date
from restaurant.models import Unit, PartnerPackage
from order.models import Order, Rating, OrderItem
from order import views
from menu.models import MenuOfTheDay

def __user_has_profile(user):
    if not user.is_authenticated() or user.is_anonymous() : return None
    try:
        user.get_profile()
        return None
    except:
        return redirect('profiles_create_profile')


def index(request):
    if 'django_language' not in request.session:
         request.session['django_language'] = 'ro'
    units = Unit.objects.annotate(avg_quality=Avg('order__rating__quality')).\
        annotate(avg_speed=Avg('order__rating__delivery_time')).\
        annotate(comment_count=Count('order__rating__feedback')).\
        order_by('?')
    user = request.user
    has_profile = __user_has_profile(user)
    if has_profile != None: return has_profile
    menu_items = ('supe', 'pizza', 'paste', 'salate', 'principal', 'desert')
    if not user.is_authenticated() or user.get_profile().is_filled():
        return render_to_response('restaurant/index.html', {
                                  'menu_items': menu_items,
                                  }, context_instance=RequestContext(request))
    else:
        return redirect('profiles_create_profile')

@render_to('restaurant/unit_list.html')
def unit_list(request):
    units = Unit.objects.annotate(avg_quality=Avg('order__rating__quality')).\
        annotate(avg_speed=Avg('order__rating__delivery_time')).\
        annotate(comment_count=Count('order__rating__feedback')).\
        order_by('?')
    return {'units': units, 'gold': units.filter(name='GL'), 'platinum': units.filter(name='PL')}

@login_required
@render_to('restaurant/unit_detail.html')
def unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    motd = unit.get_motd()
    if motd.exists(): motd = motd[0]
    else: motd = None
    return {'object': unit, 'motd': motd, 'we_are_in_unit_detail': True}

@login_required
@render_to('restaurant/comments.html')
def unit_comments(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    return {'ratings': Rating.objects.filter(order__unit__id = unit.id)}

@user_passes_test(lambda u: u.is_authenticated() and u.is_staff)
@render_to('restaurant/package_history.html')
def package_history(request, unit_id):
    history = PartnerPackage.objects.filter(unit__id=unit_id)
    return {'history':history}

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
        grand_total = (total_amount_sum * unit.get_package().rate/100) + unit.get_package().monthly_fee
    else:
        grand_total = unit.get_package().monthly_fee
    return {'unit': unit, 'orders': last_month_orders, 'total_sum': total_amount_sum, 'grand_total': grand_total}
