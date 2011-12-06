from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.db.models import Sum, Avg, Count
from django.db.models import Q
from annoying.decorators import render_to
from datetime import date
from restaurant.models import Unit, PartnerPackage
from order.models import Order, Rating, OrderItem
from order import views
from menu.models import MenuOfTheDay
from userprofiles.models import BonusTransaction
from order.views import __is_restaurant_administrator
from restaurant.forms import InvoiceForm
from django.core.urlresolvers import reverse

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
    units = Unit.objects.filter(active=True).annotate(avg_quality=Avg('order__rating__quality')).\
        annotate(avg_speed=Avg('order__rating__delivery_time')).\
        annotate(comment_count=Count('order__rating__feedback')).\
        order_by('?')
    return {'units': units}#, 'gold': units.filter(name='GL'), 'platinum': units.filter(name='PL')}

@login_required
@render_to('restaurant/unit_detail.html')
def unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    motd = unit.get_motd()
    unit_carts = [key.split(':',1)[0] for key in request.session.keys()\
        if (key.split(':',1)[0].isdigit() and key.split(':',1)[0] != unit_id and len(request.session[key])>0)]
    # the last one checks if there are actual products in the cart
    if len(unit_carts) > 0:
        unit_names = Unit.objects.filter(id__in=unit_carts).values_list('id', 'name')
        msg = "You have more product added at the following restaurants: "
        for u_id, u_name in unit_names:
            msg += '<a href="%s">%s</a> ' % (reverse('restaurant:detail', kwargs={'unit_id': u_id}), u_name)
        messages.warning(request, msg)
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

@login_required
@render_to('restaurant/invoice.html')
def invoice(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    __is_restaurant_administrator(request, unit)
    end = today = date.today()
    start = today.replace(day=1)    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']            
    else:
        form = InvoiceForm(initial={'start_date':start, 'end_date':today})
    orders = Order.objects.filter(unit=unit).filter(creation_date__range=(start, end)).filter(status__in=['ST', 'RV', 'DL'])
    total_sum = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    bonuses = BonusTransaction.objects.filter(order__unit=unit).filter(order__creation_date__range=(start, end)).filter(amount__lt=0)
    total_bonus = bonuses.aggregate(Sum('amount'))['amount__sum'] or 0    
    package = unit.partnerpackage_set.filter(start_date__lte=start).filter(Q(end_date__gte=end) | (Q(end_date=None) & Q(current=True)))
    if package.exists() and package.count() == 1:
        package = package[0]
    else:
        if package.count() > 1:
            messages.error(request, _('Multiple packages found for selected period!'))
        else:
            messages.error(request, _('No (unique) partner package found for selected time range!'))
        grand_total = 0
        tva_grand_total = 0
        return locals()
    
    if total_sum != None:
        grand_total = (total_sum * package.rate/100) + package.monthly_fee + package.menu_management_fee + total_bonus
    else:
        grand_total = package.monthly_fee + package.menu_management_fee
    tva_grand_total = grand_total * 1.24            
    return locals()
