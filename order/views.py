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
import csv
from geopy import distance
from order.models import Order, OrderItem
from restaurant.models import Unit
from menu.models import Item
from order.forms import CartNameForm, OrderForm, RatingForm
from userprofiles.models import DeliveryAddress
from bonus.models import Bonus

def __get_current_order(request, unit):
    try:
        co = Order.objects.filter(user=request.user).filter(status='CR').get(unit__id=unit.id)
        if co.is_abandoned():
            raise
    except:
        unit = Unit.objects.get(pk=unit.id)
        co = Order.objects.create(user=request.user, unit=unit, employee_id=unit.employee_id)
    return co

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
        queryset = Order.objects.filter(user__id=request.user.id).exclude(status='CR')[:50]
    )

@login_required
def list_unit(request, unit_id):
    return list_detail.object_list(
        request,
        queryset = Order.objects.filter(user__id=request.user.id).filter(unit=unit_id).exclude(status='CR')[:50],
        template_name = 'order/order_list_div.html',
    )


@login_required
def add_item(request, item_id, cart_name):
    if cart_name.startswith("cart-"):
        cart_name = cart_name.split("cart-")[1]
    item = get_object_or_404(Item, pk=item_id)
    try:
        current_order = __get_current_order(request, item.unit)
        if current_order.status != 'CR': HttpResponseForbidden(_('Please focus on something productive!'))
        if cart_name == '': cart_name = request.user.username
        order_item = OrderItem.objects.filter(order=current_order).filter(item=item).filter(cart=cart_name)
        if order_item.exists():
            order_item = order_item[0]
            order_item.count += 1
            order_item.save()
        else:
            order_item = OrderItem.objects.create(order=current_order, item=item, cart=cart_name)
        return HttpResponse(str(order_item.id))
    except:
        raise Http404()

@login_required
def add_topping(request, master_id, item_id, cart_name):
    if cart_name.startswith("cart-"):
        cart_name = cart_name.split("cart-")[1]
    item = get_object_or_404(Item, pk=item_id)
    try:
        current_order = __get_current_order(request, item.unit)
        if current_order.status != 'CR': HttpResponseForbidden(_('Please focus on something productive!'))
        if cart_name == '': cart_name = request.user.username
        master_item = OrderItem.objects.filter(order=current_order).filter(item__id=master_id).filter(cart=cart_name)
        if master_item.exists():
            master_item = master_item[0]
        order_item = OrderItem.objects.filter(order=current_order).filter(master=master_item).filter(item=item).filter(cart=cart_name)
        if order_item.exists():
            order_item = order_item[0]
            order_item.count += 1
            order_item.save()
        else:
            order_item = OrderItem.objects.create(order=current_order, item=item, cart=cart_name, master=master_item)
        return HttpResponse(str(order_item.id))
    except:
        raise Http404()

@login_required
def remove_item(request, item_id):
    oi = get_object_or_404(OrderItem, pk=item_id)
    if oi.order.status != 'CR': HttpResponseForbidden(_('Please focus on something productive!'))
    if oi.count > 1:
        oi.count -= 1
        oi.save()
        return HttpResponse(str(oi.count))
    else:
        oi.delete()
        return HttpResponse('nook')

@login_required
@render_to('order/order_div.html')
def get_current_order(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    return {'order': __get_current_order(request, unit)}


@login_required
def send(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    current_order = __get_current_order(request, unit)
    if current_order.status != 'CR':
        messages.warning(request, _('Current order already sent.'))
        return redirect('order:timer', order_id=current_order.id)
    try:
        if  not unit.schedule.is_open():
            messages.error(request, _('This restaurant is now closed! Please check the open hours and come back later.'))
            return redirect('restaurant:detail', unit_id=unit.id)
    except:
        messages.error(request, _('This restaurant is now closed! Please check the open hours and come back later.'))
        return redirect('restaurant:detail', unit_id=unit.id)
    if unit.minimum_ord_val > current_order.total_amount:
        messages.error(request, _('This restaurant has a minimum order value of %(min)d') % {'min': unit.minimum_ord_val})
        return redirect('restaurant:detail', unit_id=unit.id)    
    if current_order.address:
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
            order.status = 'ST'
            order.save()
            messages.warning(request, _('Your order has been sent to the restaurant!'))
            send_mail('New Order',
                       render_to_string('order/mail_order_detail.html', {'order': order}, context_instance=RequestContext(request)),
                       'bucatar@filemaker-solutions.ro',
                       [unit.email],
                       fail_silently=False)
            return redirect('order:timer', order_id=current_order.id)
    else:
        form = OrderForm(instance=current_order)
    form.fields['address'] = forms.ModelChoiceField(queryset=DeliveryAddress.objects.filter(user=request.user), required=True, initial={'primary': True})
    return render_to_response('order/send_confirmation.html', {
                                  'form': form,
                                  'order': current_order,
                                  }, context_instance=RequestContext(request))

@login_required
def add_cart(request, order_id):
  if request.method == 'POST':
      form = CartNameForm(request.POST)
      if form.is_valid(): # All validation rules pass
          next_cart = request.POST['name']
          return HttpResponse('<li><a id="cart-%s" href="%s">%s</a></li> ' % (next_cart, reverse('order:get_cart', args=[order_id, next_cart]), next_cart))
  else:
      form = CartNameForm() # An unbound form
  return render_to_response('order/cart_name.html', {
        'form': form,
        'order_id': order_id,
    }, context_instance=RequestContext(request))

@login_required
@render_to('order/order_cart.html')
def get_cart(request, order_id, cartname):
    if cartname.startswith("cart-"):
        cartname = cartname.split("cart-")[1]
    order = get_object_or_404(Order, pk=order_id)
    oil = OrderItem.objects.filter(order__id=order.id).filter(cart=cartname)
    return {'order': order, 'cartname': cartname, 'oil': oil}

@login_required
def get_total_amount(request, order_id):
  order = get_object_or_404(Order, pk=order_id)
  return HttpResponse(str(order.total_amount))

@login_required
def get_subtotal(request, unit_id, cart_name):
  unit = get_object_or_404(Unit, pk=unit_id)
  current_order = __get_current_order(request, unit)
  return HttpResponse(str(current_order.get_cart_subtotal(cart_name)))

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
    orders = Order.objects.filter(unit=unit_id).filter(status__in=['ST', 'RV'])
    return {'order_list': orders, 'unit_id': unit_id}

@login_required
@render_to('order/restaurant_order_list_div.html')
def restlist_ajax(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    __is_restaurant_administrator(request, unit)
    orders = Order.objects.filter(unit=unit_id).filter(status__in=['ST', 'RV'])
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
            # create bonus
            b  = Bonus(user = order.user)
            b.set_rating_bonus()
            b.save()
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
def get_available_toppings(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    order = __get_current_order(request, unit)
    items = ["top%s" % oi.item_id for oi in order.orderitem_set.exclude(item__toppings__isnull=True)]
    return {'items': items}
