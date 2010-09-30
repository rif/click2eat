from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

class DeliveryArea(models.Model):
    name = models.CharField(_('name'), max_length=200)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
      verbose_name = _('Delivery Area')
      verbose_name_plural = _('Deliver Areas')

class Communication(models.Model):
    name = models.CharField(_('name'), max_length=200)
    
    def __unicode__(self):
        return self.name

    class Meta:
      verbose_name = _('Communication')
      verbose_name_plural = _('Communication')

class PartnerPackage(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), help_text=_('The css class for this package'))
    details = models.TextField(_('details'))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
      verbose_name = _('Partner Package')
      verbose_name_plural = _('Partner Packages')

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
    
    def __unicode__(self):
        return self.name
    
    class Meta:
      verbose_name = _('Employee')
      verbose_name_plural = _('Employees')

class Unit(models.Model):
    name = models.CharField(_('name'), max_length=50)
    address = models.CharField(_('address'), max_length=200)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=15)
    logo_path = models.ImageField(_('logo path'), upload_to="restaurant_logos", null=True, blank=True)
    unit_devlivery = models.ForeignKey(DeliveryArea, verbose_name=_('unit delivery'))
    currency = models.ForeignKey(Currency, verbose_name=_('accepted currencies'), related_name='units_using_this')
    overall_discount = models.FloatField(_('overall_discount'))
    latitude = models.FloatField(_('latitude'))
    longitude = models.FloatField(_('longitude'))
    delivery_time = models.IntegerField(_('delivery time'))
    communication = models.ManyToManyField(Communication, verbose_name=_('communication'))
    package = models.ForeignKey(PartnerPackage, verbose_name=_('package'))
    open_hours = models.CharField(_('open_hours'), max_length=10)
    minimum_ord_val = models.IntegerField(_('minimum order value'))
    payment_method = models.ManyToManyField(PaymentMethod, verbose_name=_('payment method'))
    employee = models.ForeignKey(Employee, verbose_name=_('employee'), help_text=_('The internal employee responsible for this unit.'))
    contact_person = models.CharField(_('contact persoon'), max_length=50)    
    delivery_time_user = models.FloatField(_('delivery time user'), null=True, blank=True, help_text=_('Calculated as a avg from user feedback.'))
    delivery_type = models.ForeignKey(DeliveryType, verbose_name=_('delivery type'))
    admin_users = models.CharField(_('admin users'), max_length=100, null=True, blank=True, help_text=_('the users that can access front-end administration pages for this unit.'))
    info = models.TextField(_('info'), null=True, blank=True)
    active = models.BooleanField(_('active'), default=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
      verbose_name = _('Unit')
      verbose_name_plural = _('Units')

def rating_range(value):
    if value < 0 or value > 5:
        raise ValidationError(_('Value must be in the range [0,5]'))

class Rating(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    restaurant = models.ForeignKey(Unit, verbose_name=_('restaurant'))
    quality = models.SmallIntegerField(_('quality'), validators=[rating_range], help_text=_('0 worst quality, 5 highest quality'))
    delivery_time = models.SmallIntegerField(_('delivery time'), validators=[rating_range], help_text=_('0 worst delivery time, 5 best delivery time'))
    feedback = models.TextField(_('feedback'), null=True, blank=True)

    class Meta:
      verbose_name = _('Rating')
      verbose_name_plural = _('Ratings')
