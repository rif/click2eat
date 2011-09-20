from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from restaurant.models import Unit, DeliveryType
from menu.models import Item, Topping, MenuOfTheDay
from order.models import Order, OrderItem
from bonus.models import Bonus, BONUS_PERCENTAGE
from userprofiles.models import DeliveryAddress
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
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
        if __have_unit_cart(request, unit_id):
          count = __count_cart_sum(request, unit_id)
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
        show_toppings = False
        for cn in __get_cart_names(request, unit_id):
          if item_id in request.session[cn]:
            show_toppings = True
            break
        if __have_unit_cart(request, unit_id):
          count = __count_cart_sum(request, unit_id)
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/motd.html')
def motd(request):
        motds = MenuOfTheDay.objects.filter(day = date.today());
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def shop(request, cart_name, item_id):
        item, unit_id = __get_payload(item_id)
        cn = '%s:%s' % (unit_id, cart_name)
        if cn not in request.session and '_' in item_id: #first added item is a topping
            return {'error': '2e62'} # kriptic errors for hackers delight :)
        if cn in request.session and '_' in item_id and item_id.split('_',1)[0] not in request.session[cn]: # added topping without item
            return {'error': '2e6z'}
        if cn not in request.session:
          request.session[cn] = {}
        if item_id not in request.session[cn]:
          request.session[cn][item_id] = [1, item.get_price(), item.get_name()]
        else:
          request.session[cn][item_id][0] += 1
        request.session.modified = True
        return {'count': __count_cart_sum(request, cn)}

@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def decr_item(request, cart_name, unit_id, item_id):
        cn = '%s:%s' % (unit_id, cart_name)
        if cn in request.session:
          if request.session[cn][item_id][0] > 1:
            request.session[cn][item_id][0] -= 1
          else:
            del request.session[cn][item_id]
            for top in [k for k in request.session[cn].keys() if item_id + '_' in k]:
              del request.session[cn][top]
        request.session.modified = True
        return {'count': __count_cart_sum(request,cn)}


@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def incr_item(request, cart_name, unit_id, item_id):
        cn = '%s:%s' % (unit_id, cart_name)
        if cn in request.session:
            request.session[cn][item_id][0] += 1
            request.session.modified = True
        return {'count': __count_cart_sum(request,cn)}

@login_required(login_url='/mobile/accounts/login/')
@render_to('mobile/shopping_cart.html')
def shopping_cart(request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        total_sum = 0
        if __have_unit_cart(request, unit_id):
          total_sum = __count_cart_sum(request,unit_id)
          carts = []
          for cn in __get_cart_names(request,unit_id):
            carts.append((cn.split(':',1)[1],request.session[cn]))
        return locals()

@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def send_order(request, unit_id):
        if not __have_unit_cart(request, unit_id): return {'error': '2e45'} # kriptic errors for hackers delight :)
        unit = get_object_or_404(Unit, pk=unit_id)
        if not unit.is_open(): return {'error': '2e61'}
        if unit.minimum_ord_val > __count_cart_sum(request, unit_id): return {'error': '2e65'}
        address = get_object_or_404(DeliveryAddress, pk=request.GET['da'])
        delivery_type = get_object_or_404(DeliveryType, pk=request.GET['dt'])
        order = Order.objects.create(user=request.user, unit=unit, employee_id=unit.employee_id, address=address, delivery_type=delivery_type, status='ST')
        for cn in __get_cart_names(request, unit_id):
          cart = request.session[cn]
          for item_id, values in cart.iteritems():
            if item_id.startswith('m'):
              motd = get_object_or_404(MenuOfTheDay, pk=item_id[1:])
              OrderItem.objects.create(order=order, menu_of_the_day=motd, count=values[0], old_price=motd.get_price(), cart=unit_id)
            elif '_' in item_id:
              top = get_object_or_404(Topping, pk=item_id.split('_',1)[1])
              master = order.orderitem_set.get(item=item_idsplit('_',1)[0])
              OrderItem.objects.create(master=master, order=order, topping=top, count=values[0], old_price=top.get_price(), cart=unit_id)
            else:
              item = get_object_or_404(Item, pk=item_id)
              OrderItem.objects.create(order=order, item=item, count=values[0], old_price=item.get_price(), cart=cn.split(':')[1])
          #give bonus to the friend
          initial_friend = order.user.get_profile().get_initial_friend()
          if initial_friend:
            b = Bonus.objects.create(user=initial_friend, from_user=order.user, money=(order.total_amount * BONUS_PERCENTAGE / 100))
          del request.session[cn]
        send_mail(_('New Order'),
                       render_to_string('order/mail_order_detail.txt', {'order': order}, context_instance=RequestContext(request)),
                       'office@filemaker-solutions.ro',
                       [unit.email],
                       fail_silently=False)
        return {}

@login_required(login_url='/mobile/accounts/login/')
@ajax_request
def cart_total(request, cart_name):
  return __count_cart_sum(request, cart_name)

def __get_cart_names(request, unit_id):
  return [key for key in request.session.keys() if key.split(':',1)[0] == unit_id]

def __have_unit_cart(request, unit_id):
  return len(__get_cart_names(request, unit_id)) > 0

def __count_cart_sum(request, cart_name):
  if ':' in cart_name:
    s = sum([v[0]*v[1] for v in request.session[cart_name].itervalues()])
  else:
    s = 0
    for cn in __get_cart_names(request, cart_name):
      s += sum([v[0]*v[1] for v in request.session[cn].itervalues()])
  return round(s,2)

def __get_payload(item_id):
  item, unit_id = None,None
  if item_id.startswith('m'):
    item = get_object_or_404(MenuOfTheDay, pk=item_id[1:])
    unit_id = item.unit_id
  elif '_' in item_id:
    item = get_object_or_404(Topping, pk=item_id.split('_',1)[1])
    unit_id = item.topping_group.unit_id
  else:
    item = get_object_or_404(Item, pk=item_id)
    unit_id = item.item_group.unit_id
  return item, str(unit_id)