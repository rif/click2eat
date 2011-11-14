from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import menu
from datetime import datetime

class Order(models.Model):
    STATUS_CHOICES = (
      ('ST', _('Sent')),
      ('RV', _('Received')),
      ('DL', _('Delivered')),
      ('CN', _('Canceled')),
    )
    user = models.ForeignKey(User, verbose_name=_('user'), editable=False)
    address = models.ForeignKey('userprofiles.DeliveryAddress', verbose_name=_('address'), null=True, blank=True)
    delivery_type = models.ForeignKey('restaurant.DeliveryType', verbose_name=_('delivery type'), null=True, blank=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    status = models.CharField(_('status'), max_length=2, choices=STATUS_CHOICES, default='ST')
    total_amount = models.FloatField(_('total amount'), default=0)
    unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'), editable=False)
    additional_info = models.TextField(_('additional info'), null=True, blank=True, help_text=_('Add here any relevant information.'))
    employee = models.ForeignKey('restaurant.Employee', verbose_name=_('employee'), help_text=_('The internal employee responsible for this order.'))
    hidden = models.BooleanField(_('hidden'))
    desired_delivery_time = models.DateTimeField(_('desired delivery time'), null=True, blank=True, help_text=_('Request this to order for a later time (yyyy-mm-dd hh:mm).'))
    paid_with_bonus = models.BooleanField(_('paid with bonus'))

    def update_total_amount(self):
        total = 0
        for oi in self.orderitem_set.iterator():
            total += oi.count * oi.old_price
        self.total_amount = round(total,2)
        self.save()

    def get_cart_subtotal(self, cart):
      subtotal = 0
      for oi in self.orderitem_set.filter(cart=cart).iterator():
        subtotal += oi.count * oi.old_price
      return round(subtotal,2)

    def get_carts(self):
        carts_dict = {}
        ois = OrderItem.objects.select_related().filter(order__id=self.id)
        carts = ois.values_list('cart', flat=True).distinct()
        for cart in carts:
            carts_dict[cart] = ois.filter(cart=cart)
        return carts_dict

    def clone(self):
        new_order = Order.objects.create(user=self.user, status='ST', unit_id=self.unit_id, employee_id=self.employee_id)
        for oi in self.orderitem_set.iterator():
            new_oi = OrderItem.objects.create(order=new_order, item=oi.item, count=oi.count, old_price=oi.item.get_price(), cart=oi.cart)
        return new_order

    def get_priority_class(self):
        delta = (self.desired_delivery_time - datetime.now()).seconds / 3600
        if delta <= 1: return "red"
        elif delta > 1 and delta < 6: return "yellow"
        else: return "green"

    def __unicode__(self):
        return self.get_status_display()

    @models.permalink
    def get_absolute_url(self):
        return ('order:detail', [str(self.id)])

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Order')
        ordering = ['-creation_date']

class OrderItem(models.Model):
    master = models.ForeignKey('self', verbose_name=_('master'), null=True, blank=True)
    order = models.ForeignKey(Order, verbose_name=_('order'))
    item = models.ForeignKey('menu.Item', verbose_name=_('item'), null=True)
    topping = models.ForeignKey('menu.Topping', verbose_name=_('topping'), null=True)
    variation = models.ForeignKey('menu.Variation', verbose_name=_('variation'), null=True)
    menu_of_the_day = models.ForeignKey('menu.MenuOfTheDay', verbose_name=_('menu of the day'), null=True)
    count = models.IntegerField(_('count'), default=1)
    old_price = models.FloatField(_('price'), default=0)
    cart = models.CharField(_('cart'), max_length=15, null=True, blank=True)

    def __unicode__(self):
        return str(self.count) + ' x item from ' + str(self.cart)

    def save(self, *args, **kwargs):
        if not self.id:
            if self.item :
                self.old_price = self.item.get_price()
            if self.topping :
                self.old_price = self.topping.price
            if self.menu_of_the_day:
                self.old_price = self.menu_of_the_day.price
            if self.variation:
                self.old_price = self.variation.price
        super(OrderItem, self).save(*args, **kwargs)
        self.order.update_total_amount()

    def get_payload(self):        
        if self.item_id:
            return self.item
        if self.topping_id:
            return self.topping
        if self.menu_of_the_day_id:          
            return self.menu_of_the_day

    def delete(self, *args, **kwargs):
        ex_order = self.order
        super(OrderItem, self).delete(*args, **kwargs)
        ex_order.update_total_amount()

    class Meta:
      verbose_name = _('Order Item')
      verbose_name_plural = _('Order Items')

class Rating(models.Model):
    RATING_CHOICES = (
      ('1', _('Very Poor')),
      ('2', _('Not that bad')),
      ('3', _('Average')),
      ('4', _('Good')),
      ('5', _('Perfect')),
    )
    user = models.ForeignKey(User, verbose_name=_('user'))
    order = models.OneToOneField(Order, verbose_name=_('order'))
    quality = models.CharField(_('quality'), max_length=1, choices=RATING_CHOICES, default='3')
    delivery_time = models.CharField(_('delivery time'), max_length=2, choices=RATING_CHOICES, default='3')
    feedback = models.TextField(_('feedback'), null=True, blank=True)

    class Meta:
      verbose_name = _('Rating')
      verbose_name_plural = _('Ratings')
