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
      ('SV', 'Served'),
      ('CA', 'Canceled'),
    )
    user = models.ForeignKey(User, verbose_name=_('user'), editable=False)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    status = models.CharField(_('status'), max_length=2, choices=STATUS_CHOICES, editable=False, default='CR')
    total_amount = models.FloatField(_('total amount'), default=0)
    unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'),)

    def update_total_ammount(self):
        total = 0
        for oi in self.orderitem_set.iterator():
            total += oi.item.price
        self.total_amount = total
        self.save()

    def is_abandoned(self):
        delta = datetime.now() - self.creation_date
        if delta.days > 1:
            if self.total_amount > 0:
              self.status = 'AB'
              self.save()
            else:
              self.delete()
            return True
        return False

    def __unicode__(self):
        self.is_abandoned()
        return unicode(self.creation_date) + " - " + self.get_status_display()

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Order')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'))
    item = models.ForeignKey('menu.Item', verbose_name=_('item'))
    cart = models.CharField(_('cart'), max_length=15, null=True, blank=True)

    def __unicode__(self):
        return str(self.order) + " : " + str(self.item)

    def save(self, *args, **kwargs):
        super(OrderItem, self).save(*args, **kwargs) # Call the "real" save() method.
        self.order.update_total_ammount()

    class Meta:
      verbose_name = _('Order Item')
      verbose_name_plural = _('Order Items')