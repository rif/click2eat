from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.sites.models import Site
from django import forms
from django.views.generic import list_detail
from annoying.decorators import render_to, ajax_request
import csv
from order.models import Order
from restaurant.models import Unit, DeliveryType
from order.forms import OrderForm, RatingForm
from userprofiles.models import DeliveryAddress
from order.tasks import send_email_task
from shopping_service import OrderCarts, construct_order
from geopy import distance

def __is_restaurant_administrator(request, unit):
    if request.user.username == 'admin': return
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
@render_to('order/send_confirmation.html')
def confirm_order(request, unit_id):
    oc = OrderCarts(request.session,unit_id)
    unit = oc.get_unit()
    total_sum = oc.get_total_sum()
    oc.update_prices()
    oc.check_and_show_odd_promotion_message(request)
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
            paid_with_bonus = 'paid_with_bonus' in form.data
            construct_order(request, oc, unit, order, paid_with_bonus)
            if not unit.is_open():
                return redirect('restaurant:detail', unit_id=unit.id)
            return redirect('order:timer', order_id=order.id)
    else:
        form = OrderForm()
    form.fields['delivery_type'] = forms.ModelChoiceField(unit.delivery_type.all(), required=True, initial={'primary': True})
    form.fields['address'] = forms.ModelChoiceField(queryset=DeliveryAddress.objects.filter(user=request.user), required=True, initial={'primary': True})
    try:
        profile = request.user.get_profile()
        show_pay_with_bonus = profile and profile.get_current_bonus() > total_sum    
        if show_pay_with_bonus:
            messages.info(request, _('Congratulations! You have enough bonus to pay for your order. Please check "Pay using bonus" to use it.'))
            form.fields['paid_with_bonus'] = forms.BooleanField(label=_('Pay using bonus'), help_text=_('We shall use the minimum number of received bonuses enough to cover the order total amount'), required=False)
    except: # if the user does not have userprofile then forget it
        pass
    return locals()

@login_required
@render_to('order/timer.html')
def timer(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return {'order': order}

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
    subject = _('Click2eat: Order sent to you!')
    body = render_to_string('order/confirmation_email.txt', {'order': order, 'site_name': Site.objects.get_current().domain}, context_instance=RequestContext(request)),
    send_from = order.unit.email
    send_to = (order.user.email,)
    send_email_task.delay(subject, body[0], send_from, send_to)
    return HttpResponse(order.get_status_display())

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
