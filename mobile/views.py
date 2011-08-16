from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from restaurant.models import Unit
from django.shortcuts import get_object_or_404

#@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/units.html')
def units(request):
	units = Unit.objects.all()
	return dict(units = units)

#@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/menu.html')
def menu(request, unit_id):
	unit = get_object_or_404(Unit, pk=unit_id)
	return dict(unit = unit)