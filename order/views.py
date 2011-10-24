from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.db.models import Sum
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.sites.models import Site
from django import forms
from django.views.generic import list_detail
from annoying.decorators import render_to, ajax_request
import csv
from datetime import datetime
from geopy import distance
from order.models import Order, OrderItem
from restaurant.models import Unit, DeliveryType
from menu.models import Item, Topping, MenuOfTheDay
from order.forms import CartNameForm, OrderForm, RatingForm
from userprofiles.models import DeliveryAddress
from bonus.models import Bonus, BONUS_PERCENTAGE
from order.tasks import send_email_task

def __is_restaurant_administrator(request, unit):
    if not unit.admin_users: raise PermissionDenied()
    admin_user_list = [u.strip() for u in unit.admin_users.split(",")]
    if request.user.username not in admin_user_list:
        raise PermissionDenied()

@login_required
def limited_object_detail(*args, **kwargs):
    request = args[0]
    queryset = kwargs['queryset']
    object_id = kwargs['object_id']
    ord = queryset.get(pk=object_id)
    if ord.user_id != request.user.id:
        raise PermissionDenied()
    return list_detail.object_detail(*args, **kwargs)

@login_required
def list(request):
    return list_detail.object_list(
        request,
        queryset = Order.objects.filter(user__id=request.user.id).exclude(hidden=True)[:50]
    )

@login_required
def list_unit(request, unit_id):
    return list_detail.object_list(
        request,
        queryset = Order.objects.filter(user__id=request.user.id).filter(unit=unit_id).exclude(hidden=True)[:50],
        template_name = 'order/order_list_div.html',
    )



@login_required
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
        return {'total': __count_cart_sum(request, unit_id),
            'subtotal': __count_cart_sum(request, cn),
            'id':item_id,
            'price':item.get_price(),
            'name':item.get_name()}

@login_required
@ajax_request
def decr_item(request, cart_name, unit_id, item_id):
        cn = '%s:%s' % (unit_id, cart_name)
        if cn in request.session and item_id in request.session[cn]:
          if request.session[cn][item_id][0] > 1:
            request.session[cn][item_id][0] -= 1
            count = request.session[cn][item_id][0]
            unit_price = request.session[cn][item_id][1]            
            subtotal = __count_cart_sum(request,cn)
          else:
            count = 0
            unit_price = 0
            del request.session[cn][item_id]
            """ Delete assocaited toppings """
            for top in [k for k in request.session[cn].keys() if item_id + '_' in k]:
              del request.session[cn][top]              
            subtotal = __count_cart_sum(request,cn)
            """ Delete the cart if all the items are removed """
            if len(request.session[cn]) == 0: 
              del request.session[cn]          
          request.session.modified = True
          total = __count_cart_sum(request,unit_id)
          return {'total': total,
                'subtotal': subtotal,
                'count': count,
                'itemtotal': count * unit_price}
        return {'error': '29a'}


@login_required
@ajax_request
def incr_item(request, cart_name, unit_id, item_id):
        cn = '%s:%s' % (unit_id, cart_name)
        if cn in request.session and item_id in request.session[cn]:
            request.session[cn][item_id][0] += 1
            request.session.modified = True
            count = request.session[cn][item_id][0]
            unit_price = request.session[cn][item_id][1]
            return {'total': __count_cart_sum(request,unit_id),
                'subtotal': __count_cart_sum(request,cn),
                'count': count,
                'itemtotal': count * unit_price}
        return {'error': '29a'}

@login_required
@render_to('order/shopping_cart.html')
def shopping_cart(request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        if not __have_unit_cart(request, unit_id):               
			cn = '%s:%s' % (unit_id, request.user.username)
			request.session[cn] = {}
        total_sum = __count_cart_sum(request,unit_id)
        show_confirm_order = True
        carts = []
        for cn in __get_cart_names(request,unit_id):
        	carts.append((cn.split(':',1)[1], request.session[cn], __count_cart_sum(request, cn)))
        return locals()

@login_required
@ajax_request
def send_order(request, unit_id):
        if not __have_unit_cart(request, unit_id): return {'error': '2e45'} # kriptic errors for hackers delight :)
        unit = get_object_or_404(Unit, pk=unit_id)
        if not unit.is_open(): return {'error': '2e61'}
        if unit.minimum_ord_val > __count_cart_sum(request, unit_id): return {'error': '2e65'}
        if 'dt' not in request.GET: return {'error': '2e77'}        
        delivery_type = get_object_or_404(DeliveryType, pk=request.GET['dt'])
        if delivery_type.require_address and 'da' not in request.GET: return {'error': '2e78'}  
        if 'da' in request.GET:
            address = get_object_or_404(DeliveryAddress, pk=request.GET['da'])        
        order = Order(address=address, delivery_type=delivery_type)
        __construct_order(request, unit, order)                        
        return {}

def __construct_order(request, unit, order):    
    order.user = request.user
    order.employee_id=unit.employee_id
    order.unit = unit
    if not order.desired_delivery_time:
        order.desired_delivery_time = datetime.now()
    order.save() # save it to be able to bind OrderItems
    unit_id = str(unit.id)
    for cn in __get_cart_names(request, unit_id):        
        cart = request.session[cn]
        for item_id in sorted(cart.keys()): # sorting to get the items before the toppings
            values = cart[item_id]            
            if item_id.startswith('m'):
              motd = get_object_or_404(MenuOfTheDay, pk=item_id[1:])
              OrderItem.objects.create(order=order, menu_of_the_day=motd, count=values[0], old_price=motd.get_price(), cart=unit_id)
            elif '_' in item_id:
              top = get_object_or_404(Topping, pk=item_id.split('_',1)[1])         
              master = order.orderitem_set.get(item__id=item_id.split('_',1)[0])
              OrderItem.objects.create(master=master, order=order, topping=top, count=values[0], old_price=top.get_price(), cart=unit_id)
            else:
              item = get_object_or_404(Item, pk=item_id)
              OrderItem.objects.create(order=order, item=item, count=values[0], old_price=item.get_price(), cart=cn.split(':')[1])
        del request.session[cn]
    #give bonus to the friend
    initial_friend = order.user.get_profile().get_initial_friend()
    if initial_friend:
        b = Bonus.objects.create(user=initial_friend, from_user=order.user, money=round((order.total_amount * BONUS_PERCENTAGE / 100),2))
    subject = _('New Order')
    body = render_to_string('order/mail_order_detail.txt', {'order': order}, context_instance=RequestContext(request))    
    send_from = 'office@click2eat.ro'
    send_to = (order.unit.email,)   
    send_email_task.delay(subject, body, send_from, send_to)
    
def _consume_bonus(order):
    amount = order.total_amount
    bonuses = Bonus.objects.filter(user__id = order.user_id).filter(used=False).order_by('received_date')
    total = bonuses.aggregate(Sum('money'))
    total = round(total['money__sum'],2)
    if amount > total: return -1
    sum = 0
    now = datetime.now()
    for bonus in bonuses:
        if sum < amount:
            sum += bonus.money
            bonus.used = True
            bonus.used_date = now
            bonus.save()
        else:
            break
    order.paid_with_bonus = True
    order.save()    
    return 0
    
@login_required
@render_to('order/send_confirmation.html')
def confirm_order(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    total_sum = __count_cart_sum(request,unit_id)    
    carts = []
    for cn in __get_cart_names(request,unit_id):
        carts.append((cn.split(':',1)[1], request.session[cn], __count_cart_sum(request, cn)))    
    if not unit.is_open():
        messages.warning(request, _('This restaurant is now closed! Please check the open hours and set desired delivery time accordingly.'))
    if unit.minimum_ord_val > total_sum:
        messages.error(request, _('This restaurant has a minimum order value of %(min)d') % {'min': unit.minimum_ord_val})
        return redirect('restaurant:detail', unit_id=unit.id)
    """if current_order.address and not current_order.address.geolocation_error:
        src = (unit.latitude, unit.longitude)
        dest = (current_order.address.latitude, current_order.address.longitude)
        dist = distance.distance(src, dest)
        if  dist.km > unit.delivery_range:
            messages.warning(request, _('We are sorry, you are not in the delivery range of this restaurant.'))
            return redirect('restaurant:detail', unit_id=unit.id)"""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        form.unit = unit
        if form.is_valid():
            order = form.save(commit=False)
            __construct_order(request, unit, order) 
            if 'paid_with_bonus' in form.data:
                _consume_bonus(order)
            if not unit.is_open():
                return redirect('restaurant:detail', unit_id=unit.id)
            return redirect('order:timer', order_id=order.id)
    else:
        form = OrderForm()
    form.fields['delivery_type'] = forms.ModelChoiceField(unit.delivery_type.all(), required=True, initial={'primary': True})
    form.fields['address'] = forms.ModelChoiceField(queryset=DeliveryAddress.objects.filter(user=request.user), required=True, initial={'primary': True})
    show_pay_with_bonus = request.user.get_profile() and request.user.get_profile().get_bonus_money() > total_sum
    if show_pay_with_bonus:
        messages.info(request, _('Congratulations! You have enough bonus to pay for your order. Please check "Pay using bonus" to use it.'))
        form.fields['paid_with_bonus'] = forms.BooleanField(label=_('Pay using bonus'), help_text=_('We shall use the minimum number of received bonuses enough to cover the order total amount'), required=False)
    return locals()

@login_required
@ajax_request
def clear(request, unit_id):
    for cn in __get_cart_names(request, unit_id):
        del request.session[cn]
    return dict(response='done!')

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

@login_required
@render_to('order/timer.html')
def timer(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return {'order': order}

@login_required
def clone(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    current_order = __get_current_order(request, order.unit)
    current_order.delete()
    new_order = order.clone()
    if new_order.total_amount != order.total_amount:
        messages.add_message(request, messages.WARNING, _('The price of some items has changed. Please review the order!'))
    return redirect('restaurant:detail', unit_id=order.unit_id)

@login_required
@render_to('order/restaurant_order_list.html')
def restlist(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    __is_restaurant_administrator(request, unit)
    orders = Order.objects.filter(unit=unit_id).filter(status__in=['ST', 'RV']).order_by('desired_delivery_time')
    return {'order_list': orders, 'unit_id': unit_id, 'orderstitle': _('Current orders')}

@login_required
@render_to('order/restaurant_order_list_div.html')
def restlist_ajax(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    __is_restaurant_administrator(request, unit)
    orders = Order.objects.filter(unit=unit_id).filter(status__in=['ST', 'RV']).order_by('desired_delivery_time')
    return {'order_list': orders, 'orderstitle': _('Current orders')}

@login_required
@render_to('order/restaurant_order_list_div.html')
def restlist_history_ajax(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    __is_restaurant_administrator(request, unit)
    orders = Order.objects.filter(unit=unit_id).filter(status__in=['DL', 'CN']).order_by('creation_date')
    return {'order_list': orders, 'orderstitle': _('Order history')}

@login_required
def restlist_csv(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    __is_restaurant_administrator(request, unit)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Address', 'Date', 'Status', 'Amount', 'Additional info'])
    for o in Order.objects.filter(unit=unit_id).iterator():
        writer.writerow([o.user.get_full_name(), o.address, o.creation_date, o.get_status_display(), o.total_amount, o.additional_info])
    return response

@login_required
@render_to('order/restaurant_order_detail.html')
def restdetail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    __is_restaurant_administrator(request, order.unit)
    if order.status == 'ST':
        order.status = 'RV'
        order.save()
    return{'order': order}

@login_required
def mark_delivered(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    __is_restaurant_administrator(request, order.unit)
    order.status = 'DL'
    order.save()
    return HttpResponse(order.get_status_display())

@login_required
def send_confiramtion_email(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    __is_restaurant_administrator(request, order.unit)
    subject = _('Click2eat: Order received')
    body = render_to_string('order/confirmation_email.txt', {'order': order, 'site_name': Site.objects.get_current().domain}, context_instance=RequestContext(request)),
    send_from = order.unit.email
    send_to = (order.user.email,)   
    send_email_task.delay(subject, body[0], send_from, send_to)
    return HttpResponse('Sent!')

@login_required
def feedback(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.user != order.user:
        raise PermissionDenied()
    try:
        order.rating
        #if the rating exists exit
        messages.add_message(request, messages.INFO, _('Thank you! You already sent feedback for this order.'))
        return redirect('restaurant:index')
    except:
        pass
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            new_rating = form.save(commit=False)
            new_rating.user = order.user
            new_rating.order = order
            new_rating.save()
            messages.add_message(request, messages.INFO, _('Thank you! Your feedback is very appreciated!'))
            return redirect('restaurant:index')
    else:
        form = RatingForm()
    return render_to_response('order/feedback.html', {
                                  'form': form,
                                  'order': order,
                                  }, context_instance=RequestContext(request))

@login_required
@ajax_request
def hide(request, order_id):
    order = Order.objects.filter(user=request.user).filter(id=order_id)
    if order.exists():
        order = order[0]
        order.hidden = True
        order.save()
        return {'order_id': order.id}
    else:
        return {'order_id': -1}


@ajax_request
def is_addres_required(request, dt_id):
    dt = get_object_or_404(DeliveryType, pk=dt_id)
    return {'require_address': dt.require_address}
