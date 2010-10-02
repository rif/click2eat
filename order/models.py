from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from datetime import datetime

class Order(models.Model):
    STATUS_CHOICES = (
      ('AB', 'Abandoned'),
      ('CR', 'Created'),
      ('ST', 'Sent'),
      ('RV', 'Received'),
      ('DL', 'Delivered'),
      ('CN', 'Canceled'),
    )
    user = models.ForeignKey(User, verbose_name=_('user'), editable=False)
    address = models.ForeignKey('userprofiles.DeliveryAddress', verbose_name=_('address'), null=True, blank=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    status = models.CharField(_('status'), max_length=2, choices=STATUS_CHOICES, default='CR')
    total_amount = models.FloatField(_('total amount'), default=0)
    unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'), editable=False)
    additional_info = models.TextField(_('additional info'), null=True, blank=True, help_text=_('Add here any relevant information.'))

    def update_total_ammount(self):
        total = 0
        for oi in self.orderitem_set.iterator():
            total += oi.old_price
        self.total_amount = total
        self.save()

    def get_cart_subtotal(self, cart):
      subtotal = 0
      for oi in self.orderitem_set.filter(cart=cart).iterator():
        subtotal += oi.old_price
      return subtotal

    def is_abandoned(self):
        delta = datetime.now() - self.creation_date
        if delta.days > 0:
            if self.total_amount > 0:
              self.status = 'AB'
              self.save()
            else:
              self.delete()
            return True
        return False
    
    def get_carts(self):
        carts_dict = {}
        ois = OrderItem.objects.select_related().filter(order__id=self.id)
        carts = ois.values_list('cart', flat=True)
        unique_carts_set = set(carts)
        for cart in unique_carts_set:
            carts_dict[cart] = ois.filter(cart=cart)
        return carts_dict
    
    def clone(self):
        new_order = Order.objects.create(user=self.user, status='CR', unit=self.unit)
        for oi in self.orderitem_set.iterator():
            new_oi = OrderItem.objects.create(order=new_order, item=oi.item, old_price=oi.item.price, cart=oi.cart)
        return new_order
        

    def __unicode__(self):
        self.is_abandoned()
        return self.creation_date.strftime('%A %d%B%Y %H:%M') + ' - ' + self.get_status_display()
    
    @models.permalink
    def get_absolute_url(self):
        return ('order:detail', [str(self.id)])
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Order')
        ordering = ['-creation_date']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'))
    item = models.ForeignKey('menu.Item', verbose_name=_('item'))
    old_price = models.FloatField(_('price'), default=0)
    cart = models.CharField(_('cart'), max_length=15, null=True, blank=True)

    def __unicode__(self):
        return str(self.item)

    def save(self, *args, **kwargs):
        if not self.id:
            self.old_price = self.item.price
        super(OrderItem, self).save(*args, **kwargs)
        self.order.update_total_ammount()

    def delete(self, *args, **kwargs):
        ex_order = self.order
        super(OrderItem, self).delete(*args, **kwargs)
        ex_order.update_total_ammount()

    class Meta:
      verbose_name = _('Order Item')
      verbose_name_plural = _('Order Items')
