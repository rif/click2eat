from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse
#from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from restaurant.models import Unit


def __user_has_profile(user):
    if not user.is_authenticated(): return None
    try:
        print user.userprofile
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


def get_random_platinum(request):
    units = Unit.objects.order_by('?')
    return render_to_response('restaurant/platinum_restaurant_list.html', {
                                  'platinum': units.filter(package__slug='platinum'),
                                  }, context_instance=RequestContext(request))

def get_random_gold(request):
    units = Unit.objects.order_by('?')
    return render_to_response('restaurant/gold_restaurant_list.html', {
                                  'gold': units.filter(package__slug='gold'),
                                  }, context_instance=RequestContext(request))
