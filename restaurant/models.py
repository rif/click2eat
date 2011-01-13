from django.db import models
from datetime import datetime, date
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager

class Communication(models.Model):
    name = models.CharField(_('name'), max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
      verbose_name = _('Communication')
      verbose_name_plural = _('Communication')

class PartnerPackage(models.Model):
    PACKAGE_CHOICES = (
      ('SV', _('Silver')),
      ('GL', _('Gold')),
      ('PL', _('Platinum'))
    )
    unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))
    name = models.CharField(_('name'), max_length=2, choices=PACKAGE_CHOICES, default='SV')
    monthly_fee = models.FloatField(_('monthly fee'))
    rate = models.FloatField(_('rate'), help_text=_('The percentage taken from every order'))
    details = models.TextField(_('details'))
    start_date = models.DateField(_('start date'), auto_now_add=True)
    end_date = models.DateField(_('end date'), null=True, blank=True)
    current = models.BooleanField(_('current'))
    
    def get_class(self):
	return self.get_name_display().lower()

    def __unicode__(self):
        return self.name

    class Meta:
      verbose_name = _('Partner Package')
      verbose_name_plural = _('Partner Packages')
      ordering = ['-start_date']

class PaymentMethod(models.Model):
    name = models.CharField(_('name'), max_length=100)
    details = models.TextField(_('details'))

    def __unicode__(self):
        return self.name

    class Meta:
      verbose_name = _('Payment Method')
      verbose_name_plural = _('Payment Methods')

class Currency(models.Model):
    name = models.CharField(_('name'), max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
      verbose_name = _('Currency')
      verbose_name_plural = _('Currency')

class DeliveryType(models.Model):
    name = models.CharField(_('name'), max_length=100)
    price = models.FloatField(_('price'), )

    def __unicode__(self):
        return self.name

    class Meta:
      verbose_name = _('Delivery Type')
      verbose_name_plural = _('Delivery Types')

class Employee(models.Model):
    name = models.CharField(_('name'), max_length=100)
    address = models.CharField(_('address'), max_length=200)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=15)
    start_date = models.DateField(_('start_date'))
    end_date = models.DateField(_('end_date'))
    rate = models.FloatField(_('rate'))

    def __unicode__(self):
        return self.name

    class Meta:
      verbose_name = _('Employee')
      verbose_name_plural = _('Employees')

class Interval(models.Model):
    schedule = models.ForeignKey('Schedule', verbose_name=_('schedule'))
    weekdays = models.CommaSeparatedIntegerField(_('weekdays'), max_length=13, help_text=_('integer, comma separated, starting Monday=1 e.g. 1,2,3,4,5'))
    start_hour = models.TimeField(_('start hour'), help_text=_('e.g. 10:30:00'))
    end_hour = models.TimeField(_('end hour'), help_text=_('e.g. 15:00:00'))

    def __unicode__(self):
        return self.weekdays + ' ' + self.start_hour.strftime("%H:%M") + '-' + self.end_hour.strftime("%H:%M")

    def is_open(self):
        return self._is_open(datetime.now())

    def _is_open(self, check_date):
        now = check_date
        starth = None
        endh = None
        weekday = now.isoweekday()
        if str(weekday) not in self.weekdays:
            return False
        if self.start_hour:
            starth = datetime.strptime(now.strftime("%d-%m-%Y ") + self.start_hour.strftime("%H:%M"), "%d-%m-%Y %H:%M")
            if now < starth:
                return False
        if self.end_hour:
            endh = datetime.strptime(now.strftime("%d-%m-%Y ") + self.end_hour.strftime("%H:%M"), "%d-%m-%Y %H:%M")
            # correct after midnight end hour
            if starth and starth > endh:
                endh = datetime(endh.year, endh.month, endh.day + 1, endh.hour, endh.minute) 
            if now > endh:
                return False
        return True

    class Meta:
      verbose_name = _('Interval')
      verbose_name_plural = _('Intervals')

class Schedule(models.Model):
    description = models.CharField(_('description'), max_length=100, help_text=_('This text will appear on the frontend for open hours.'))
    unit = models.OneToOneField('Unit', verbose_name=_('unit'))

    def is_open(self):
        for interval in self.interval_set.iterator():
            if interval.is_open():
                return True
        return False

    def __unicode__(self):
        return self.description

    class Meta:
      verbose_name = _('Schedule')
      verbose_name_plural = _('Schedules')

class Unit(models.Model):
    name = models.CharField(_('name'), max_length=50)
    address = models.CharField(_('address'), max_length=200)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=15)
    mobile = models.CharField(_('mobile'), max_length=15)
    logo_path = models.ImageField(_('logo path'), upload_to="restaurant_logos", null=True, blank=True)
    currency = models.ForeignKey(Currency, verbose_name=_('accepted currencies'), related_name='units_using_this')
    overall_discount = models.FloatField(_('overall_discount'))
    latitude = models.FloatField(_('latitude'))
    longitude = models.FloatField(_('longitude'))
    delivery_range = models.FloatField(_('range'), help_text=_('Delivery range in km'))
    delivery_time = models.IntegerField(_('delivery time'))
    communication = models.ManyToManyField(Communication, verbose_name=_('communication'))
    minimum_ord_val = models.IntegerField(_('minimum order value'))
    payment_method = models.ManyToManyField(PaymentMethod, verbose_name=_('payment method'))
    employee = models.ForeignKey(Employee, verbose_name=_('employee'), help_text=_('The internal employee responsible for this unit.'))
    contact_person = models.CharField(_('contact persoon'), max_length=50)
    delivery_time_user = models.FloatField(_('delivery time user'), null=True, blank=True, editable=False, help_text=_('Calculated as a avg from user feedback.'))
    delivery_type = models.ForeignKey(DeliveryType, verbose_name=_('delivery type'))
    admin_users = models.CharField(_('admin users'), max_length=100, null=True, blank=True, help_text=_('the users that can access front-end administration pages for this unit.'))
    added_date = models.DateField(_('added date'), auto_now_add=True, editable=False)
    info = models.TextField(_('info'), null=True, blank=True)
    active = models.BooleanField(_('active'), default=True)

    tags = TaggableManager()

    def __unicode__(self):
        return self.name

    def is_new(self):
        delta = date.today() - self.added_date
        return delta.days < 7

    """ Returns true if the unit has an active promotion """
    def has_promotion(self):
        for promo in self.promotion_set.iterator:
            if promo.is_active():
                return True
        return False

    def get_avg_quality(self):
        if not self.avg_quality:
            return 0
        return unicode(self.avg_quality * 100/5)

    def get_avg_speed(self):
        if not self.avg_speed:
            return 0
        return unicode(self.avg_speed * 100/5)

    def get_package(self):
	return self.partnerpackage_set.get(current=True)

    @models.permalink
    def get_absolute_url(self):
        return ('restaurant:detail', [str(self.id)])

    class Meta:
      verbose_name = _('Unit')
      verbose_name_plural = _('Units')
