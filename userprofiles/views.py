from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic.create_update import update_object, delete_object
from django.views.generic.list_detail import object_detail
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from userprofiles.forms import DeliveryAddressForm
from userprofiles.models import DeliveryAddress

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
def limited_update_object(*args, **kwargs):
    request = args[0]
    model = kwargs['model']
    object_id = kwargs['object_id']
    addr = get_object_or_404(model, pk=object_id)
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
