from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from annoying.decorators import render_to
from menu.models import Item, MenuOfTheDay, Topping, Variation
from order.models import OrderItem, Order
from restaurant.models import Unit
from datetime import datetime
from bonus.models import BonusTransaction, BONUS_PERCENTAGE
from order.tasks import send_email_task
from django.contrib import messages

class CartItem:
    def __init__(self, item_id):
        #MasterId-VarID_TopId
        self.item_id = item_id
        self.item, self.variation, self.promotion = None, None, None
        if item_id.startswith('m'):
            item_id = item_id[1:].split('-')[0] #discard m char and variation id
            self.item = get_object_or_404(MenuOfTheDay, pk=item_id)
        elif '_' in item_id:
            id = item_id.split('_',1)[1]
            id = id.split('-')[0]     
            self.item = get_object_or_404(Topping, pk=id)    
        else:
            item_id, vari_id =  item_id.split('-',1)
            self.variation = get_object_or_None(Variation, pk=vari_id)
            self.item = get_object_or_404(Item, pk=item_id)
            self.promotion = self.item.promotion
        self.price = self.get_item_price()

    def get_item(self):
        return self.item

    def get_promotion(self):
        return self.promotion

    def set_price(self, price):
        self.price = price

    def get_price(self, no_promotion=False):
        if no_promotion:
            return self.get_item_price()
        return self.price

    def get_item_price(self):
        vid = self.variation.id if self.variation else 0
        return round(self.item.get_price(variation_id=vid), 2)

    def get_variation(self):
        return self.variation

    def get_name(self):
        vid = self.variation.id if self.variation else 0
        return self.item.get_name(variation_id=vid)
    
    def get_item_id(self):
        return self.item_id
    
    def __str__(self):
        return self.item_id


class OrderCarts:
    def __init__(self, session, unit_id):
        self.carts = {}
        self.unit_id = unit_id
        for cart in [key for key in session.keys() if key.split(':',1)[0] == unit_id]:
            items = []            
            for item in session[cart]:
                items.append(item)
            self.carts[cart] = items

    def get_carts(self, cn=None):
        return self.carts if cn is None else self.carts[cn]

    def get_cart_names(self):
        return self.carts.keys()

    def have_unit_cart(self):
        return len(self.carts.keys()) > 0
    
    def is_below_minimum(self):
        unit = self.get_unit()
        if unit is None: raise PermissionDenied()
        return self.get_total_sum() < unit.minimum_ord_val

    def get_total_sum(self, cn=None, no_promotion=False):
        if cn and cn not in self.get_cart_names():
            return 0
        if cn: s = sum([v.get_price(no_promotion) for v in self.carts[cn]])
        else:
            s = 0
            for values in self.carts.itervalues():
                s += sum([v.get_price(no_promotion) for v in values])
        return round(s, 2)
    
    def update_session(self, session):
        session.update(self.carts)
        session.modified = True

    def get_unit(self):
        return get_object_or_None(Unit, pk=self.unit_id)
    
    def get_item(self, cn, item_id):
        if cn not in self.carts:
            return None
        for item in self.carts[cn]:
            if item.get_item_id() == item_id: return item
        return None
    
    def create_cart_if_not_exists(self, cn):
        if cn not in self.carts: self.carts[cn] = []
    
    def add_item(self, cn, item_id):
        self.create_cart_if_not_exists(cn)
        self.carts[cn].append(CartItem(item_id))
    
    def decr_item(self, cn, item_id):
        item = self.get_item(cn, item_id)
        if not item: return #we have an hacker case here?
        self.carts[cn].remove(item)
        # Delete assocaited toppings
        for top in [ci for ci in self.carts[cn] if (item_id + '_') in ci.get_item_id()]:
            self.carts[cn].remove(top)
        #Delete the cart if all the items are removed
        if len(self.carts[cn]) == 0 and len(self.carts) > 1: del self.carts[cn]
    
    def __str__(self):
        result = ''
        for cn, items in self.carts.iteritems():
            result += '%s\t%s\n' %(cn, '\t\n'.join([str(i) for i in items]))
        return result

    def update_prices(self):
        multiple_item_promotions={}
        for cn, items in self.carts.iteritems():
            for item in items:
                promotion = item.get_promotion()
                if not promotion: continue
                if not promotion.is_active():
                    continue
                if promotion.total_sum_trigger > self.get_total_sum(no_promotion=True):
                    # if we are below threshold make sure we get the old price (useful when deleting items)
                    item.set_price(item.get_item_price())
                    continue
                if promotion.numer_of_items > 1:
                    # the items in the same promotion have to have the same variation
                    pair = (promotion, item.get_variation().name)
                    # if promotion spans multiple items save for later analysis
                    if pair not in multiple_item_promotions:
                        multiple_item_promotions[pair] = []
                    multiple_item_promotions[pair].append(item)
                    continue
                # we should get here if the promotion it is active, sum trigger was activated
                # and it affects only one item
                item.set_price(promotion.get_new_price(item.get_item_price()))
        self.odd_promotion_item_selection = False
        for pair, items in multiple_item_promotions.iteritems():
            promotion, variation = pair
            if len(items) % promotion.numer_of_items == promotion.numer_of_items - 1:
                # if the user only selected the paid items (or selected different variations)
                self.odd_promotion_item_selection = True
            sorted_items = sorted(items, key=lambda item: item.get_price())
            items_middle_index = len(sorted_items)/promotion.numer_of_items
            for i in range(len(sorted_items)):
                item = sorted_items[i]
                if i < items_middle_index:
                    item.set_price(promotion.get_new_price(item.get_item_price()))
                else:
                    item.set_price(item.get_item_price())

    def check_and_show_odd_promotion_message(self, request):
        mes = _('Please select the paid and bonus items from the promotion.\
         They have to have the same size for the promotion to be applied!')
        if self.odd_promotion_item_selection:
            messages.add_message(request, messages.INFO, mes)

@render_to('order/shopping_cart.html')
def shopping_cart(request, unit_id):
    #del request.session['1:rif']
    oc = OrderCarts(request.session, unit_id)
    if not oc.have_unit_cart(): oc.create_cart_if_not_exists('%s:%s' % (unit_id, request.user.username))
    we_are_are_in_cart = True
    return locals()

@login_required
@render_to('order/shopping_cart.html')
def clear(request, unit_id):
    oc = OrderCarts(request.session, unit_id)
    for cn in oc.get_cart_names():
        del request.session[cn]
    oc.get_carts().clear()
    if not oc.have_unit_cart(): oc.create_cart_if_not_exists('%s:%s' % (unit_id, request.user.username))
    we_are_are_in_cart = True
    return locals()

@login_required
@render_to('order/shopping_cart.html')
def shop(request,unit_id,  cart_name, item_id):
    oc = OrderCarts(request.session, unit_id)
    cn = '%s:%s' % (unit_id, cart_name)

    if cn not in oc.get_carts() and '_' in item_id: #first added item is a topping
        return {'error': '2e62'} # kriptic errors for hackers delight :)
    #if cn in oc.get_carts() and '_' in item_id and item_id.rsplit('_')[0] not in oc.get_carts(cn): # added topping without item            
    #    return {'error': '2e6z'}

    oc.add_item(cn, item_id)
    oc.update_session(request.session)
    m = oc.update_prices()
    if m: messages.add_message(request, messages.INFO, NO_PROMOTION_MESSAGE)
    we_are_are_in_cart = True
    return locals()

@login_required
@render_to('order/shopping_cart.html')
def decr_item(request, unit_id, cart_name, item_id):
    oc = OrderCarts(request.session, unit_id)
    cn = '%s:%s' % (unit_id, cart_name)
    oc.decr_item(cn, item_id)
    oc.update_session(request.session)
    oc.update_prices()
    we_are_are_in_cart = True
    return locals()

def construct_order(request, oc, unit, order, paid_with_bonus):
    order.user = request.user
    order.employee_id=unit.employee_id
    order.unit = unit
    if not order.desired_delivery_time:
        order.desired_delivery_time = datetime.now()
    order.save() # save it to be able to bind OrderItems
    unit_id = str(unit.id)
    master, variation = None, None
    for cn, items in oc.get_carts().iteritems():
        for item in items:
            item_id = item.get_item_id()
            if item_id.startswith('m'):
              motd = item.get_item()
              OrderItem.objects.create(order=order, menu_of_the_day=motd, old_price=item.get_price(), cart=cn)
            elif '_' in item_id:
              top = get_object_or_404(Topping, pk=item_id.split('_',1)[1])
              if not master: pass # shit there is no master for this topping, figure out what to do              
              OrderItem.objects.create(master=master, order=order, topping=top, old_price=item.get_price(), cart=cn)
            else:
              item_id, vari_id =  item_id.split('-',1)
              variation = get_object_or_None(Variation, pk=vari_id)
              payload = item.get_item()
              master = OrderItem.objects.create(order=order, variation=variation, item=payload, old_price=item.get_price(), cart=cn)
        del request.session[cn]
    #give bonus to the friend
    if paid_with_bonus:
        consume_bonus(order)
    try:
        initial_friend = order.user.get_profile().get_initial_friend()
        if initial_friend and not order.paid_with_bonus:
            BonusTransaction.objects.create(user=initial_friend, order=order, amount=round((order.total_amount * BONUS_PERCENTAGE / 100),2))
    except: # if the user does not have userprofile then forget it
        pass
    subject = _('New Order')
    body = render_to_string('order/mail_order_detail.txt', {'order': order}, context_instance=RequestContext(request))
    send_from = 'office@click2eat.ro'
    send_to = (order.unit.email,)
    send_email_task.delay(subject, body, send_from, send_to)

def consume_bonus(order):
    amount = order.total_amount    
    user = order.user
    if not user.get_profile(): return -2    
    if amount > user.get_profile().get_current_bonus(): return -1
    BonusTransaction.objects.create(user=order.user, order=order, amount=-round(amount,2))   
    order.paid_with_bonus = True
    order.save()
    return 0

@login_required
def clone(request, order_id):
    order = Order.objects.select_related().filter(pk=order_id)
    if not order: raise PermissionDenied()
    order = order[0]
    # check if it is his order
    if order.user_id != request.user.id: raise PermissionDenied()
    oc = OrderCarts(request.session, order.unit_id)
    for cn in oc.get_cart_names():
        del request.session[cn]
    oc.get_carts().clear()
    carts = oc.get_carts()
    for oi in order.orderitem_set.iterator():
        cart = oi.cart
        if not cart or ':' not in cart:
            cart = '%s:%s' % (oc.unit_id, oi.cart or request.user.username)
        if cart not in carts:
            carts[cart] = []
        #MasterId-VarID_TopId
        if oi.master is None:
            carts[cart].append(CartItem('%s-%s' % (oi.get_payload().get_id(), oi.variation_id or '0',)))
        else:
            carts[cart].append(CartItem('%s-%s_%s' % (oi.master.get_payload().get_id(), oi.variation or '0',oi.get_payload().get_id())))
    oc.update_session(request.session)
    oc.update_prices()
    if oc.get_total_sum() != order.total_amount:
        messages.add_message(request, messages.WARNING, _('The price of some items has changed. Please review the order!'))
    return redirect('restaurant:detail', unit_id=oc.unit_id)
