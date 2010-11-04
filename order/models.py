from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
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
    employee = models.ForeignKey('restaurant.Employee', verbose_name=_('employee'), help_text=_('The internal employee responsible for this order.'))

    def update_total_amount(self):
        total = 0
        for oi in self.orderitem_set.iterator():
            total += oi.count * oi.old_price
        self.total_amount = total
        self.save()

    def get_cart_subtotal(self, cart):
      subtotal = 0
      for oi in self.orderitem_set.filter(cart=cart).iterator():
        subtotal += oi.count * oi.old_price
      return subtotal

    def is_abandoned(self):
        if self.status in ('ST', 'RV', 'DL', 'CN'):
            return False
        if self.status == 'AB':
            return True
        # if status is CR 
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
        carts = ois.values_list('cart', flat=True).distinct()
        for cart in carts:
            carts_dict[cart] = ois.filter(cart=cart)
        return carts_dict

    def clone(self):
        new_order = Order.objects.create(user=self.user, status='CR', unit_id=self.unit_id, employee_id=self.employee_id)
        for oi in self.orderitem_set.iterator():
            new_oi = OrderItem.objects.create(order=new_order, item=oi.item, count=oi.count, old_price=oi.item.get_price(), cart=oi.cart)
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
    count = models.IntegerField(_('count'), default=1)
    old_price = models.FloatField(_('price'), default=0)
    cart = models.CharField(_('cart'), max_length=15, null=True, blank=True)

    def __unicode__(self):
        return str(self.item)

    def save(self, *args, **kwargs):
        if not self.id:
            self.old_price = self.item.get_price()
        super(OrderItem, self).save(*args, **kwargs)
        self.order.update_total_amount()

    def delete(self, *args, **kwargs):
        ex_order = self.order
        super(OrderItem, self).delete(*args, **kwargs)
        ex_order.update_total_amount()

    class Meta:
      verbose_name = _('Order Item')
      verbose_name_plural = _('Order Items')

def rating_range(value):
    if value < 0 or value > 5:
        raise ValidationError(_('Value must be in the range [0,5]'))

class Rating(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    order = models.OneToOneField(Order, verbose_name=_('order'))
    quality = models.SmallIntegerField(_('quality'), validators=[rating_range], help_text=_('0 worst quality, 5 highest quality'))
    delivery_time = models.SmallIntegerField(_('delivery time'), validators=[rating_range], help_text=_('0 worst delivery time, 5 best delivery time'))
    feedback = models.TextField(_('feedback'), null=True, blank=True)

    class Meta:
      verbose_name = _('Rating')
      verbose_name_plural = _('Ratings')
