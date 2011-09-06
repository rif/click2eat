from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from restaurant.models import Unit
from menu.models import Item
from django.shortcuts import get_object_or_404

#@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/units.html')
def units(request):
	units = Unit.objects.all()
	return locals()

#@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/menu.html')
def menu(request, unit_id):
	unit = get_object_or_404(Unit, pk=unit_id)
	return locals()

@render_to('mobile/search.html')
def search(request):
        items = Item.objects.select_related('tags', 'item_group', 'item_group__unit')
        return locals()

@render_to('mobile/item_detail.html')
def item_detail(request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        return locals()