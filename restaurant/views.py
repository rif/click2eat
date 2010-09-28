from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from restaurant.models import Unit
from restaurant.forms import RatingForm
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
def unit_detail(request, object_id):
    unit = get_object_or_404(Unit, pk=object_id)
    current_order = views.__get_current_order(request, unit)
    return render_to_response('restaurant/unit_detail.html', {
                                  'object': unit,
                                  'order': current_order,
                                  'carts': current_order.get_carts(),
                                  }, context_instance=RequestContext(request))

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

def feedback(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            new_rating = form.save(commit=False)
            new_rating.user = request.user
            new_rating.restaurant = unit
            new_rating.save()
            return redirect('restaurant:index')
    else:
        form = RatingForm()

    return render_to_response('restaurant/feedback.html', {
                                  'form': form,
                                  }, context_instance=RequestContext(request))