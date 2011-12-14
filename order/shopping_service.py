from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from menu.models import Item, Topping, Variation
from restaurant.models import Unit

class CartItem:
    def __init__(self, item_id, count = 0):
        #mMasterId-VarID_TopId
        self.count, self.item_id = count, item_id
        uid, item_id = item_id.split('!')
        self.item, self.variation = None,None
        if item_id.startswith('m'):
            item_id = item_id[1:].split('-')[0] #discard m char and variation id
            self.item = get_object_or_404(MenuOfTheDay, pk=item_id)
        elif '_' in item_id:
            id = item_id.split('_',1)[1]
            id = id.split('-')[0]     
            self.item = get_object_or_404(Topping, pk=id)    
        else:
            if '-' in item_id: # we have a variation
                item_id, vari_id =  item_id.split('-',1)        
                self.variation = get_object_or_None(Variation, pk=vari_id)
            self.item = get_object_or_404(Item, pk=item_id)

    def set_count(self, count):
        self.count = count
    
    def get_count(self):
        return self.count

    def get_item(self):
        return self.item

    def get_price(self):
        vid = self.variation.id if self.variation else 0
        return self.item.get_price(variation_id=vid)
    
    def get_total(self):
        return self.count * self.get_price()

    def get_name(self):
        vid = self.variation.id if self.variation else 0
        return self.item.get_name(variation_id=vid)
    
    def get_item_id(self):
        return self.item_id

    def get_session_value():
        return self.item_id, self.get_count()
    
    def __str__(self):
        return '%s: %d' % (self.item_id, self.count)


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
        return self.carts if cn == None else self.carts[cn]

    def get_cart_names(self):
        return self.carts.keys()

    def have_unit_cart(self):
        return len(self.carts.keys()) > 0

    def get_total_sum(self, cn=None):
        if cn: s = sum([v.get_total() for v in self.carts[cn]])
        else:
            s = 0
            for values in self.carts.itervalues():
              s += sum([v.get_total() for v in values])
        return round(s, 2)
    
    def update_session(self, session):
        session.update(self.carts)
        session.modified = True

    def get_unit(self):
        return get_object_or_None(Unit, pk=self.unit_id)
    
    def get_item(self, cn, item_id):
        for item in self.carts[cn]:
            if item.get_item_id() == item_id: return item
        return None
    
    def create_cart_if_not_exists(self, cn):
        if cn not in self.carts: self.carts[cn] = []
    
    def add_item(self, cn, item_id):
        self.create_cart_if_not_exists(cn)
        self.carts[cn].append(CartItem(item_id, 1))
    
    def decr_item(self, cn, item_id):
        item = self.get_item(cn, item_id)
        if not item: return #we have an hacker case here?
        if item.get_count() > 1:
            item.set_count(item.get_count() - 1)
        else:                
            self.carts[cn].remove(item)
            """ Delete assocaited toppings """
            for top in [ci for ci in self.carts[cn] if (item_id + '_') in ci.get_item_id()]:
                self.carts[cn].remove(top)
            """ Delete the cart if all the items are removed """
            if len(self.carts[cn]) == 0 and len(self.carts) > 1: del self.carts[cn]

    def incr_item(self, cn, item_id):
        item = self.get_item(cn, item_id)
        if item: item.set_count(item.get_count() + 1)
    
    def __str__(self):
        result = ''
        for cn, items in self.carts.iteritems():
            result += '%s\t%s\n' %(cn, '\t\n'.join([str(i) for i in items]))
        return result


@render_to('order/shopping_cart.html')
def shopping_cart(request, unit_id):
    #del request.session['1:rif']
    oc = OrderCarts(request.session, unit_id)
    if not oc.have_unit_cart(): oc.create_cart_if_not_exists('%s:%s' % (unit_id, request.user.username))
    show_confirm_order = True
    return locals()

@login_required
@render_to('order/shopping_cart.html')
def shop(request,unit_id,  cart_name, item_id):       
    oc = OrderCarts(request.session,unit_id)
    cn = '%s:%s' % (unit_id, cart_name)

    if cn not in oc.get_carts() and '_' in item_id: #first added item is a topping
        return {'error': '2e62'} # kriptic errors for hackers delight :)
    #if cn in oc.get_carts() and '_' in item_id and item_id.rsplit('_')[0] not in oc.get_carts(cn): # added topping without item            
    #    return {'error': '2e6z'}

    oc.add_item(cn, item_id)
    oc.update_session(request.session)
    show_confirm_order = True
    return locals()

@login_required
@render_to('order/shopping_cart.html')
def decr_item(request, unit_id, cart_name, item_id):
    oc = OrderCarts(request.session,unit_id)
    cn = '%s:%s' % (unit_id, cart_name)
    oc.decr_item(cn, item_id)
    oc.update_session(request.session)
    show_confirm_order = True
    return locals()


@login_required
@render_to('order/shopping_cart.html')
def incr_item(request,  unit_id, cart_name, item_id):
    oc = OrderCarts(request.session,unit_id)
    cn = '%s:%s' % (unit_id, cart_name)
    oc.incr_item(cn, item_id)
    oc.update_session(request.session)
    show_confirm_order = True
    return locals()

def construct_order(request, unit, order, paid_with_bonus):
    order.user = request.user
    order.employee_id=unit.employee_id
    order.unit = unit
    if not order.desired_delivery_time:
        order.desired_delivery_time = datetime.now()
    order.save() # save it to be able to bind OrderItems
    unit_id = str(unit.id)
    master = None
    for cn in __get_cart_names(request, unit_id):
        cart = request.session[cn]
        for item_id in cart.keys():
            values = cart[item_id]
            item_id = item_id.split('_', 1)            
            if item_id.startswith('m'):
              motd = get_object_or_404(MenuOfTheDay, pk=item_id[1:])
              OrderItem.objects.create(order=order, menu_of_the_day=motd, count=values[0], old_price=motd.get_price(), cart=unit_id)
            elif '_' in item_id:
              top = get_object_or_404(Topping, pk=item_id.split('_',1)[1])
              if not master: pass # shit there is no master for this topping, figure out what to do              
              OrderItem.objects.create(master=master, order=order, topping=top, count=values[0], old_price=top.get_price(), cart=unit_id)
            else:              
              if '-' in item_id: # we have a variation
                  item_id, vari_id =  item_id.split('-',1)        
                  variation = get_object_or_None(Variation, pk=vari_id)                            
              item = get_object_or_404(Item, pk=item_id)              
              if variation: price = variation.price
              else: price = item.get_price()                            
              master = OrderItem.objects.create(order=order, variation=variation, item=item, count=values[0], cart=cn.split(':')[1])                        
        del request.session[cn]
    #give bonus to the friend
    if paid_with_bonus:
        _consume_bonus(order)
    try:
        initial_friend = order.user.get_profile().get_initial_friend()
        if initial_friend and not order.paid_with_bonus:
            b = BonusTransaction.objects.create(user=initial_friend, order=order, amount=round((order.total_amount * BONUS_PERCENTAGE / 100),2))
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