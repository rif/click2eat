from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from restaurant.models import Unit
from userprofiles.models import UserProfile
def index(request):
    units = Unit.objects.order_by('?')
    user = request.user
    try:
        if not user.is_authenticated() or user.get_profile().is_filled():
            return render_to_response('restaurant/index.html', {
                                                                'units': units,
                                                                'gold': units.filter(package__slug='gold'),
                                                                'platinum': units.filter(package__slug='platinum'),
                                                                }, context_instance=RequestContext(request))
        else:
            return redirect('profiles_create_profile')
    except User.DoesNotExist:
        return redirect('profiles_create_profile')

    