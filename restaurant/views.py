from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from annoying.decorators import render_to
from restaurant.models import Unit
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
def unit_detail(request, object_id):
    unit = get_object_or_404(Unit, pk=object_id)
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
