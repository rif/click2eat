from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse
#from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from userprofiles.forms import DeliveryAddressForm

@login_required
def create(request):
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect('userprofiles:address_detail', object_id=new_addres.id)
    else:
        form = DeliveryAddressForm()

    return render_to_response('userprofiles/deliveryaddress_form.html', {
        'form': form,
    }, context_instance=RequestContext(request))
