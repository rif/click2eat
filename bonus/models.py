from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from order.models import Order

BONUS_PERCENTAGE = 0.5

class BonusTransaction(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    from_user = models.ForeignKey(User, verbose_name=_('from user'), related_name='bonus_given_set', null=True, blank=True)
    order = models.ForeignKey(Order, verbose_name=_('order'), null=True, blank=True)
    transaction_date = models.DateTimeField(_('transaction date'), auto_now_add=True, editable=False)
    amount = models.FloatField(_('amount'))
    
    class Meta:
      verbose_name = _('Bonus Transaction')
      verbose_name_plural = _('Bonus Transactions')
      ordering = ['-transaction_date']

