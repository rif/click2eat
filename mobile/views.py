from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from django.shortcuts import get_object_or_404
from restaurant.models import Unit
from menu.models import Item, MenuOfTheDay
from order.shopping_service import OrderCarts
from datetime import date

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/units.html')
def units(request):
        units = Unit.objects.all()
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/menu.html')
def menu(request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        oc = OrderCarts(request.session, unit_id)
        cn = '%s:%s' % (unit_id,  request.user.username)
        total = oc.get_total_sum(cn)
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/search.html')
def search(request):
        items = Item.objects.select_related('tags', 'item_group', 'item_group__unit')
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/item_detail.html')
def item_detail(request, unit_id, item_id):
        item = get_object_or_404(Item, pk=item_id)
        cn = '%s:%s' % (unit_id,  request.user.username)
        oc = OrderCarts(request.session, unit_id)
        total = oc.get_total_sum(cn)
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/motd.html')
def motd(request):
        motds = MenuOfTheDay.objects.filter(day = date.today());
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/shopping_cart.html')
def shopping_cart(request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        oc = OrderCarts(request.session, unit_id)
        cn = '%s:%s' % (unit_id,  request.user.username)
        total = oc.get_total_sum(cn)
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def shop(request, unit_id, item_id):
    print "test"
    oc = OrderCarts(request.session, unit_id)
    cn = '%s:%s' % (unit_id, request.user.username)

    if cn not in oc.get_carts() and '_' in item_id: #first added item is a topping
        return {'error': '2e62'} # kriptic errors for hackers delight :)
        #if cn in oc.get_carts() and '_' in item_id and item_id.rsplit('_')[0] not in oc.get_carts(cn): # added topping without item
    #    return {'error': '2e6z'}

    oc.add_item(cn, item_id)
    oc.update_session(request.session)
    oc.update_prices()
    return {'total': oc.get_total_sum()}

@login_required
@render_to('mobile/shopping_cart.html')
def decr_item(request, unit_id, item_id):
    oc = OrderCarts(request.session, unit_id)
    cn = '%s:%s' % (unit_id, request.user.username)
    oc.decr_item(cn, item_id)
    oc.update_session(request.session)
    oc.update_prices()
    we_are_are_in_cart = True
    return locals()


@login_required
@render_to('mobile/shopping_cart.html')
def incr_item(request,  unit_id, item_id):
    oc = OrderCarts(request.session, unit_id)
    cn = '%s:%s' % (unit_id, request.user.username)
    oc.incr_item(cn, item_id)
    oc.update_session(request.session)
    oc.update_prices()
    we_are_are_in_cart = True
    return locals()