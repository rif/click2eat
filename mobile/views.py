from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from django.shortcuts import get_object_or_404
from restaurant.models import Unit
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
        count = 0
        if views.__have_unit_cart(request, unit_id):
          count = views.__count_cart_sum(request, unit_id)
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
        count = 0
        show_toppings = False
        for cn in views.__get_cart_names(request, unit_id):
          if item_id in request.session[cn]:
            show_toppings = True
            break
        if views.__have_unit_cart(request, unit_id):
          count = views.__count_cart_sum(request, unit_id)
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
        total_sum = 0
        if views.__have_unit_cart(request, unit_id):
          total_sum = views.__count_cart_sum(request,unit_id)
          carts = []
          for cn in views.__get_cart_names(request,unit_id):
            carts.append((cn.split(':',1)[1],request.session[cn]))
        return locals()
