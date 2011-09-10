from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from restaurant.models import Unit
from menu.models import Item, MenuOfTheDay
from django.shortcuts import get_object_or_404
from datetime import date

@login_required(login_url='/mobile/accounts/login/')
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
        cart_name = item.item_group.unit.name + 'cart'
        count = 0
        if cart_name in request.session:
          count = __count_cart_items(request.session[cart_name])
        return locals()

@render_to('mobile/motd.html')
def motd(request):
        motds = MenuOfTheDay.objects.filter(day = date.today());
        return locals()

@ajax_request
def shop(request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        cart_name = item.item_group.unit.name + 'cart'
        if not cart_name in request.session:
          request.session[cart_name] = {}
        if not item.id in request.session[cart_name]:
          request.session[cart_name][item.id] = [1]
        else:
          request.session[cart_name][item.id][0] += 1
        request.session.modified = True
        return {'count': __count_cart_items(request.session[cart_name])}


@render_to('mobile/shopping_cart.html')
def shopping_cart(request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        cart_name = unit.name+'cart'
        order_items = []
        if cart_name in request.session:
          cart = request.session[cart_name]
          items = Item.objects.filter(id__in=cart.keys())
          for item in items.iterator():
            order_items.append((item, cart[item.id][0], item.price*cart[item.id][0]))
        return {'order_items': order_items}

def __count_cart_items(cart):
        return sum([v[0] for v in cart.itervalues()])