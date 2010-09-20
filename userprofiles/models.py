from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class DeliveryAddress(models.Model):
  primary = models.BooleanField(_('primary'))
  city = models.CharField(_('city'), max_length=50)
  street = models.CharField(_('street'), max_length=50)
  house_number = models.CharField(_('house number'), max_length=5)
  street_number = models.CharField(_('street number'), max_length=5,null=True,blank=True)
  floor = models.SmallIntegerField(_('floor'), )
  ap_number = models.SmallIntegerField(_('apartment number'), )
  additional_info = models.TextField(_('additional info'), null=True, blank=True)
  
  class Meta:
      verbose_name = _('Delivery Address')
      verbose_name_plural = _('Delivery Addresses')

class UserProfile(models.Model):
  GENDER_CHOICES = (
      ('M', 'Male'),
      ('F', 'Female'),
  )
  user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
  phone = models.CharField(_('phone'), max_length=15)
  newsletter = models.BooleanField(_('newsletter'), help_text=_("Do you want to receive our newsletter?"))
  sex = models.CharField(_('sex'), max_length=1, choices=GENDER_CHOICES)
  birth_date = models.DateField(_('birth date'))
  delivery_address = models.ForeignKey('DeliveryAddress', verbose_name=_('delivery address'))

  def is_filled(self):
      return self.phone != '' or self.sex != '' or self.birthday != ''

  @models.permalink
  def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
  
  class Meta:
      verbose_name = _('User Profile')
      verbose_name_plural = _('User Profiles')
    