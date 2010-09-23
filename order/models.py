from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Order(models.Model):
    STATUS_CHOICES = (
      ('AB', 'Abandoned'),
      ('ST', 'Sent'),
      ('RV', 'Received'),
      ('DL', 'Delivered'),
      ('SV', 'Served'),
      ('CA', 'Canceled'),
    )
    user = models.ForeignKey(User, verbose_name=_('user'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    status = models.CharField(_('status'), max_length=2, choices=STATUS_CHOICES, editable=False)
    total_amount = models.FloatField(_('total amount'))
    unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'),)
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Order')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'))
    item = models.ForeignKey('menu.Item', verbose_name=_('item'))
    
    class Meta:
      verbose_name = _('Order Item')
      verbose_name_plural = _('Order Items')