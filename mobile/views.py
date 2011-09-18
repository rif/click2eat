from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from restaurant.models import Unit, DeliveryType
from menu.models import Item, Topping, MenuOfTheDay
from order.models import Order, OrderItem
from bonus.models import Bonus, BONUS_PERCENTAGE
from userprofiles.models import DeliveryAddress
from django.shortcuts import get_object_or_404
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
        if unit_id in request.session:
          count = __count_cart_sum(request.session[unit_id])
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/search.html')
def search(request):
        items = Item.objects.select_related('tags', 'item_group', 'item_group__unit')
        return locals()

def motd_detail(request, motd_id):
        return item_detail(request, 'm'+motd_id)

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/item_detail.html')
def item_detail(request, item_id):
        item, unit_id = __get_payload(item_id)
        count = 0
        cart = None
        if unit_id in request.session:
          cart = request.session[unit_id]
        if unit_id in request.session:
          count = __count_cart_sum(cart)
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/motd.html')
def motd(request):
        motds = MenuOfTheDay.objects.filter(day = date.today());
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def shop(request, item_id):
        item, unit_id = __get_payload(item_id)
        if not unit_id in request.session:
          request.session[unit_id] = {}
        if not item_id in request.session[unit_id]:
          request.session[unit_id][item_id] = [1, item.get_price(), item.get_name()]
        else:
          request.session[unit_id][item_id][0] += 1
        request.session.modified = True
        return {'count': __count_cart_sum(request.session[unit_id])}

@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def decr_item(request, unit_id, item_id):
        if unit_id in request.session:
          if request.session[unit_id][item_id][0] > 1:
            request.session[unit_id][item_id][0] -= 1
          else:
            del request.session[unit_id][item_id]
            for top in [k for k in request.session[unit_id].keys() if item_id + '_' in k]:
              del request.session[unit_id][top]
        request.session.modified = True
        return {'count': __count_cart_sum(request.session[unit_id])}


@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def incr_item(request, unit_id, item_id):
        if unit_id in request.session:
            request.session[unit_id][item_id][0] += 1
        request.session.modified = True
        return {'count': __count_cart_sum(request.session[unit_id])}

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/shopping_cart.html')
def shopping_cart(request, unit_id):
        order_items = []
        unit = get_object_or_404(Unit, pk=unit_id)
        total_sum = 0
        if unit_id in request.session:
          total_sum = __count_cart_sum(request.session[unit_id])
          cart = request.session[unit_id]
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def send_order(request, unit_id):
        cart = request.session[unit_id]
        unit = get_object_or_404(Unit, pk=unit_id)
        address = get_object_or_404(DeliveryAddress, pk=request.GET['da'])
        delivery_type = get_object_or_404(DeliveryType, pk=request.GET['dt'])
        order = Order.objects.create(user=request.user, unit=unit, employee_id=unit.employee_id, address=address, delivery_type=delivery_type, status='ST')
        for item_id, values in cart.iteritems():
          if item_id.startswith('m'):
            motd = get_object_or_404(MenuOfTheDay, pk=item_id[1:])
            OrderItem.objects.create(order=order, menu_of_the_day=motd, count=values[0], old_price=motd.get_price(), cart=unit_id)
          elif '_' in item_id:
            top = get_object_or_404(Topping, pk=item_id[item_id.find('_')+1:])
            master = order.orderitem_set.get(item=item_id[:item_id.find('_')])
            OrderItem.objects.create(master=master, order=order, topping=top, count=values[0], old_price=top.get_price(), cart=unit_id)
          else:
            item = get_object_or_404(Item, pk=item_id)
            OrderItem.objects.create(order=order, item=item, count=values[0], old_price=item.get_price(), cart=unit_id)
        #give bonus to the friend
        initial_friend = order.user.get_profile().get_initial_friend()
        if initial_friend:
          b = Bonus.objects.create(user=initial_friend, from_user=order.user, money=(order.total_amount * BONUS_PERCENTAGE / 100))
        if unit_id in request.session:
          del request.session[unit_id]
        return {}



def __count_cart_sum(cart):
        return sum([v[0]*v[1] for v in cart.itervalues()])

def __get_payload(item_id):
  item, unit_id = None,None
  if item_id.startswith('m'):
    item = get_object_or_404(MenuOfTheDay, pk=item_id[1:])
    unit_id = item.unit_id
  elif '_' in item_id:
    item = get_object_or_404(Topping, pk=item_id[item_id.find('_')+1:])
    unit_id = item.topping_group.unit_id
  else:
    item = get_object_or_404(Item, pk=item_id)
    unit_id = item.item_group.unit_id
  return item, str(unit_id)