from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from django.core.exceptions import ValidationError

class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), editable=False)
    primary = models.BooleanField(_('primary'), help_text=_('Is this your most frequent used address?'))
    city = models.CharField(_('city'), max_length=50)
    street = models.CharField(_('street'), max_length=50)
    house_number = models.CharField(_('house number'), max_length=5)
    street_number = models.CharField(_('street number'), max_length=5, null=True, blank=True)
    floor = models.SmallIntegerField(_('floor'),)
    ap_number = models.SmallIntegerField(_('apartment number'),)
    additional_info = models.TextField(_('additional info'), null=True, blank=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), {'username': self.user.username})
    
    def __unicode__(self):
        """if self.primary:
            postfix = u' primary address'
        else:
            postfix = u' alternative address'
        return self.user.get_full_name() + postfix"""
        return self.get_full_address()
    
    def get_full_address(self):
        return _('%(street)s %(house_number)s floor %(floor)d ap. %(ap)d, %(city)s') % {'street': self.street, 'house_number': self.house_number, 'floor': self.floor, 'ap': self.ap_number, 'city': self.city}
    
    def save(self, *args, **kwargs):
        if self.primary == True:
            da = DeliveryAddress.objects.filter(user__id=self.user_id).filter(primary=True)
            if da.count() > 0:
              da.update(primary=False)  
        super(DeliveryAddress, self).save(*args, **kwargs) # Call the "real" save() method.
  
    class Meta:
        ordering = ['-primary']
        verbose_name = _('Delivery Address')
        verbose_name_plural = _('Delivery Addresses')

class UserProfile(models.Model):
    GENDER_CHOICES = (
                      ('M', 'Male'),
                      ('F', 'Female'),
                      )
    user = models.OneToOneField(User, verbose_name=_('user'))
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    phone = models.CharField(_('phone'), max_length=15)
    sex = models.CharField(_('sex'), max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(_('birth date'))
    newsletter = models.BooleanField(_('newsletter'), help_text=_("Do you want to receive our newsletter?"))
    communication = models.ManyToManyField('restaurant.Communication', verbose_name=_('communication'))
  
    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def is_filled(self):
        return self.first_name != '' or self.last_name != '' or self.phone != '' or self.sex != '' or self.birthday != ''

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), {'username': self.user.username})
  
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

def user_profile_handler(sender, ** kwargs):
    newProfile = kwargs['instance']
    user = newProfile.user
    user.first_name = newProfile.first_name
    user.last_name = newProfile.last_name
    user.save()

post_save.connect(user_profile_handler, sender=UserProfile)
