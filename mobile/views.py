from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from django.shortcuts import get_object_or_404
from restaurant.models import Unit
from menu.models import Item
from order import views
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
        cn = '%s:%s' % (unit_id,  request.user.username)
        total = 0
        if cn in request.session:
          total = views.__count_cart_sum(request, cn)
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/search.html')
def search(request):
        items = Item.objects.select_related('tags', 'item_group', 'item_group__unit')
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/item_detail.html')
def item_detail(request, item_id):
        item, unit_id = views.__get_payload(item_id)
        cn = '%s:%s' % (unit_id,  request.user.username)
        total = 0        
        show_toppings = False        
        if cn in request.session:
            total = views.__count_cart_sum(request, cn)
            if item_id in request.session[cn]:
                show_toppings = True                    
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
        total = 0
        cn = '%s:%s' % (unit_id,  request.user.username)
        if cn in request.session:
          total = views.__count_cart_sum(request,cn)
          cart = request.session[cn]
        return locals()
