from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.sites.models import Site
from django import forms
from django.views.generic import list_detail
from annoying.decorators import render_to, ajax_request
from django.template.defaultfilters import slugify
import csv
from datetime import datetime
from geopy import distance
from order.models import Order, OrderItem
from restaurant.models import Unit, DeliveryType
from menu.models import Item, Topping, MenuOfTheDay
from order.forms import CartNameForm, OrderForm, RatingForm
from userprofiles.models import DeliveryAddress
from bonus.models import Bonus, BONUS_PERCENTAGE


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
        queryset = Order.objects.filter(user__id=request.user.id).exclude(hidden=True).exclude(status='CR')[:50]
    )

@login_required
def list_unit(request, unit_id):
    return list_detail.object_list(
        request,
        queryset = Order.objects.filter(user__id=request.user.id).filter(unit=unit_id).exclude(hidden=True).exclude(status='CR')[:50],
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
        return {'count': __count_cart_sum(request, cn)}

@login_required
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


@login_required
@ajax_request
def incr_item(request, cart_name, unit_id, item_id):
        cn = '%s:%s' % (unit_id, cart_name)
        if cn in request.session:
            request.session[cn][item_id][0] += 1
            request.session.modified = True
        return {'count': __count_cart_sum(request,cn)}

@login_required
@render_to('order/shopping_cart.html')
def shopping_cart(request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        total_sum = 0
        if __have_unit_cart(request, unit_id):
          total_sum = __count_cart_sum(request,unit_id)
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
def send(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    current_order = __get_current_order(request, unit)
    if current_order.status != 'CR':
        messages.warning(request, _('Current order already sent.'))
        return redirect('order:timer', order_id=current_order.id)
    if not unit.is_open():
        messages.warning(request, _('This restaurant is now closed! Please check the open hours and set desired delivery time accordingly.'))
    if unit.minimum_ord_val > current_order.total_amount:
        messages.error(request, _('This restaurant has a minimum order value of %(min)d') % {'min': unit.minimum_ord_val})
        return redirect('restaurant:detail', unit_id=unit.id)
    if current_order.address and not current_order.address.geolocation_error:
        src = (unit.latitude, unit.longitude)
        dest = (current_order.address.latitude, current_order.address.longitude)
        dist = distance.distance(src, dest)
        if  dist.km > unit.delivery_range:
            messages.warning(reques, _('We are sorry, you are not in the delivery range of this restaurant.'))
            return redirect('restaurant:detail', unit_id=unit.id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=current_order)
        if form.is_valid():
            order = form.save(commit=False)
            order.creation_date = datetime.now() # update the creation time to sending time
            if order.desired_delivery_time == None:
                order.desired_delivery_time = datetime.now()
            order.status = 'ST'
            order.save()
            #give bonus to the friend
            initial_friend = order.user.get_profile().get_initial_friend()
            if initial_friend:
                b = Bonus.objects.create(user=initial_friend, from_user=order.user, money=(order.total_amount * BONUS_PERCENTAGE / 100))
            messages.warning(request, _('Your order has been sent to the restaurant!'))
            send_mail(_('New Order'),
                       render_to_string('order/mail_order_detail.txt', {'order': order}, context_instance=RequestContext(request)),
                       'office@filemaker-solutions.ro',
                       [unit.email],
                       fail_silently=False)
            if not unit.is_open():
                return redirect('restaurant:detail', unit_id=unit.id)
            return redirect('order:timer', order_id=current_order.id)
    else:
        form = OrderForm(instance=current_order)
    form.fields['delivery_type'] = forms.ModelChoiceField(current_order.unit.delivery_type.all(), required=True, initial={'primary': True})
    form.fields['address'] = forms.ModelChoiceField(queryset=DeliveryAddress.objects.filter(user=request.user), required=True, initial={'primary': True})
    return render_to_response('order/send_confirmation.html', {
                                  'form': form,
                                  'order': current_order,
                                  }, context_instance=RequestContext(request))

@login_required
@render_to('order/cart_name.html')
def add_cart(request):
  if request.method == 'POST':
      form = CartNameForm(request.POST)
      if form.is_valid(): # All validation rules pass
          next_cart = slugify(request.POST['name'])
          return {"cartname":next_cart}
  else:
      form = CartNameForm()
  return locals()

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
    return {'order_list': orders, 'unit_id': unit_id}

@login_required
@render_to('order/restaurant_order_list_div.html')
def restlist_ajax(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    __is_restaurant_administrator(request, unit)
    orders = Order.objects.filter(unit=unit_id).filter(status__in=['ST', 'RV']).order_by('desired_delivery_time')
    return {'order_list': orders}

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
        order.status = u'RV'
        order.save()
    return{'order': order}

@login_required
def mark_delivered(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    __is_restaurant_administrator(request, order.unit)
    order.status = u'DL'
    order.save()
    return HttpResponse(order.get_status_display())

@login_required
def send_confiramtion_email(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    __is_restaurant_administrator(request, order.unit)
    send_mail('Order received',
                       render_to_string('order/confirmation_email.txt',
                                          {'order': order, 'site_name': Site.objects.get_current().domain},
                                          context_instance=RequestContext(request)),
                       order.unit.email,
                       [order.user.email],
                       fail_silently=False)
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
