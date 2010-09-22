from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse
#from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from restaurant.models import Unit


def __user_has_profile(user):
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

    