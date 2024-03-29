from django.contrib.auth.models import User
from django.db import models
from geopy import geocoders
import re
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from order.models import Order
from friends.models import Friendship, JoinInvitation, Contact
from bonus.models import BonusTransaction
from restaurant.models import Unit
from django.core.validators import RegexValidator
from django.contrib.localflavor.ro.forms import ROPhoneNumberField

class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), editable=False)
    primary = models.BooleanField(_('primary'), help_text=_('Is this your most frequent used address?'))
    city = models.CharField(_('city'), max_length=50, editable=False, default='Timisoara')
    street = models.CharField(_('street'), max_length=50)
    number = models.CharField(_('number'), max_length=5)
    block = models.CharField(_('block'), max_length=5, null=True, blank=True)
    entrance = models.CharField(_('entrance'), max_length=5, null=True, blank=True)
    floor = models.SmallIntegerField(_('floor'), null=True, blank=True)
    ap_number = models.SmallIntegerField(_('apartment number'), null=True, blank=True)
    additional_info = models.TextField(_('additional info'), null=True, blank=True)
    geolocated_address = models.CharField(_('geolocated address'), max_length=200, editable=False, null=True, blank=True)
    latitude = models.FloatField(_('latitude'), default=0)
    longitude = models.FloatField(_('longitude'), default=0)
    geolocation_error = models.BooleanField(_('geolocation error'), editable=False)
    perform_geolocation = models.BooleanField(_('geolocation error'), editable=False, default=True)

    @models.permalink
    def get_absolute_url(self):
        return ('userprofiles:address_detail', (), {'object_id': self.id})

    def __unicode__(self):
        return self.get_full_address()

    def get_full_address(self):
        address = '%(street)s %(number)s' % {'street': self.street, 'number': self.number}
        if self.block:
            address += _(', bl: %s') % self.block
        if self.entrance:
            address += _(', ent: %s') % self.entrance
        if self.floor:
            address += _(', fl: %s') % self.floor
        if self.ap_number:
            address += _(', ap: %s') % self.ap_number
        if self.additional_info:
            address += _(', info: %s') % self.additional_info
        return address
    

    def save(self, *args, **kwargs):
        if self.primary == True:
            da = DeliveryAddress.objects.filter(user__id=self.user_id).filter(primary=True)
            if da.count() > 0:
              da.update(primary=False)
        if(self.perform_geolocation):
            y = geocoders.Yahoo('dj0yJmk9RUttbDF4S3BmbFo3JmQ9WVdrOVJXSjRaVkpPTm1VbWNHbzlNVEl5TWpJMU9EZzJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD1hZA--')
            nb = re.findall(r'(\d+)', self.number)
            if len(nb) > 0: nb = nb[0]
            else: nb = self.number
            try:
                self.geolocated_address, (self.latitude, self.longitude) = y.geocode("%s %s, %s, Romania" % (nb, self.street, self.city))
                self.geolocation_error = False
            except:
                self.geolocation_error = True
        self.perform_geolocation = True
        super(DeliveryAddress, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        ordering = ['-primary']
        verbose_name = _('Delivery Address')
        verbose_name_plural = _('Delivery Addresses')

class UserProfile(models.Model):
    GENDER_CHOICES = (
                      ('M', _('Male')),
                      ('F', _('Female')),
                      )
    user = models.OneToOneField(User, verbose_name=_('user'))
    first_name = models.CharField(_('first name'), max_length=50, validators=[RegexValidator(r'\A[a-zA-Z]+\Z', message=_('Only letters, please!'))])
    last_name = models.CharField(_('last name'), max_length=50, validators=[RegexValidator(r'\A[a-zA-Z]+\Z', message=_('Only letters, please!'))])
    phone = models.CharField(_('phone'), max_length=15, unique=True, validators=ROPhoneNumberField().validators)
    sex = models.CharField(_('sex'), max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    public = models.BooleanField(_('public'), help_text=_("Do you want your profile to be public?"))
    communication = models.ManyToManyField('restaurant.Communication', verbose_name=_('communication'))

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def is_filled(self):
        return self.first_name != '' or self.last_name != '' or self.phone != '' or self.sex != '' or self.birthday != ''

    def get_not_rated(self):
        return Order.objects.filter(user=self.user).filter(status__in=['ST', 'RV', 'DL']).filter(rating__isnull=True)

    def get_friends_iterator(self):
        return Friendship.objects.friends_for_user(self.user)

    def get_friends_list(self):
        return [f['friend'] for f in self.get_friends_iterator()]

    def get_initial_friend(self):
        join_invitation = JoinInvitation.objects.filter(status=5).filter(contact__email=self.user.email)
        if join_invitation.exists(): return join_invitation[0].from_user
        return None

    def get_invited_friends(self):
        return JoinInvitation.objects.filter(status=5).filter(from_user=self.user).count()

    def get_current_bonus(self):
        total = BonusTransaction.objects.filter(user__id = self.user_id).aggregate(Sum('amount'))        
        return round(total['amount__sum'] or 0, 2)

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), {'username': self.user.username})

    def administred_units(self):
        if self.user.is_staff:
            return Unit.objects.filter(active=True)
        return Unit.objects.filter(active=True).filter(admin_users__contains=self.user.username)

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
