from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Bonus(models.Model):
    REASON_CHOICES = (
      ('RT', _('You rated an order')),
      ('FR', _('Friend joined site')),
    )
    user = models.ForeignKey(User, verbose_name=_('user'))
    received_date = models.DateTimeField(_('received date'), auto_now_add=True, editable=False)
    used_date = models.DateTimeField(_('used date'), editable=False, null=True)
    used = models.BooleanField(_('used'))
    points = models.IntegerField(_('points'))
    reason = models.CharField(_('reason'), max_length=2, choices=REASON_CHOICES)
    
    def set_rating_bonus(self):
      self.reason = 'RT'
      self.points = 1

    def set_friend_bonus(self):
      self.reason = 'FR'
      self.points = 1

    class Meta:
      verbose_name = _('Bonus')
      verbose_name_plural = _('Bonus')
      ordering = ['-received_date']
