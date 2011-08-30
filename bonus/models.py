from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

BONUS_PERCENTAGE = 0.5

class Bonus(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    from_user = models.ForeignKey(User, verbose_name=_('from_user'), related_name='bonus_given_set')
    received_date = models.DateTimeField(_('received date'), auto_now_add=True, editable=False)
    used_date = models.DateTimeField(_('used date'), editable=False, null=True)
    used = models.BooleanField(_('used'))
    money = models.FloatField(_('money'))

    class Meta:
      verbose_name = _('Bonus')
      verbose_name_plural = _('Bonus')
      ordering = ['-received_date']
