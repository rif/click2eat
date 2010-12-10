from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic.create_update import update_object, delete_object
from django.views.generic.list_detail import object_detail
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from userprofiles.forms import DeliveryAddressForm
from userprofiles.models import DeliveryAddress
from annoying.utils import HttpResponseReload
from userprofiles.forms import InviteFriendForm
from profiles import views
from friends.models import JoinInvitation

@login_required
def profile_detail(request, username):
    dict = {'username': username}
    if username != request.user.username:
        dict['public_profile_field'] = 'public'
    return views.profile_detail(request, **dict)
    
@login_required
def create(request):
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect('userprofiles:address_detail', object_id=new_address.id)
    else:
        form = DeliveryAddressForm()

    return render_to_response('userprofiles/deliveryaddress_form.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def mark_geolocation_error(request, object_id):
    addr = get_object_or_404(DeliveryAddress, pk=object_id)
    if addr.user == request.user:
        addr.geolocation_error = True
        addr.perform_geolocation = False
        addr.save()
        messages.add_message(request, messages.INFO, _('Thank you, we will try to correct this.'))
    return HttpResponseReload(request)

@login_required
def invite_friend(request):
    if request.method == 'POST':
        form = InviteFriendForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            if message.strip() == "":
                message = _('Join me for lunch!')
            JoinInvitation.objects.send_invitation(request.user, email, message)
            messages.add_message(request, messages.INFO, _('The invitation email was send to %s.') % email)
            if request.is_ajax():
		return HttpResponse('ok')
	    else:
		return redirect('profiles_profile_detail', username=request.user.username)
    else:
        form = InviteFriendForm()
    if request.is_ajax():
	return render_to_response('userprofiles/invite_friend_form.html', {
	    'form': form,
	    }, context_instance=RequestContext(request))
    else:
	 return render_to_response('userprofiles/invite_friend.html', {
	    'form': form,
	    }, context_instance=RequestContext(request))


def invite_accept(request, confirmation_key):
    request.session['confirmation_key'] = confirmation_key
    return redirect('registration_register')
            
@login_required
def limited_update_object(*args, **kwargs):
    request = args[0]
    object_id = kwargs['object_id']
    addr = get_object_or_404(DeliveryAddress, pk=object_id)
    if addr.user_id != request.user.id:
        raise PermissionDenied()
    return update_object(*args, **kwargs)

@login_required
def limited_delete_object(*args, **kwargs):
    request = args[0]
    model = kwargs['model']
    object_id = kwargs['object_id']
    addr = get_object_or_404(model, pk=object_id)
    if addr.user_id != request.user.id:
        raise PermissionDenied()
    return delete_object(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
    request = args[0]
    queryset = kwargs['queryset']
    object_id = kwargs['object_id']
    addr = queryset.get(pk=object_id)
    if addr.user_id != request.user.id:
        raise PermissionDenied()
    return object_detail(*args, **kwargs)
