from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class DeliveryArea(models.Model):
    name = models.CharField(_('name'), max_length=200)
    
    class Meta:
      verbose_name = _('Delivery Area')
      verbose_name_plural = _('Deliver Areas')

class Communication(models.Model):
    name = models.CharField(_('name'), max_length=200)

    class Meta:
      verbose_name = _('Communication')
      verbose_name_plural = _('Communication')

class PartnerPackage(models.Model):
    name = models.CharField(_('name'), max_length=100)
    details = models.TextField(_('details'))
    
    class Meta:
      verbose_name = _('Partner Package')
      verbose_name_plural = _('Partner Packages')

class PaymentMethod(models.Model):
    name = models.CharField(_('name'), max_length=100)
    details = models.TextField(_('details'))
    
    class Meta:
      verbose_name = _('Payment Method')
      verbose_name_plural = _('Payment Methods')

class DeliveryType(models.Model):
    name = models.CharField(_('name'), max_length=100)
    price = models.FloatField(_('price'), )
    
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
    
    class Meta:
      verbose_name = _('Employee')
      verbose_name_plural = _('Employees')

class Unit(models.Model):
    name = models.CharField(_('name'), max_length=50)
    address = models.CharField(_('address'), max_length=200)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=15)
    unit_devlivery = models.ForeignKey(DeliveryArea, verbose_name=_('unit delivery'))
    overall_discount = models.FloatField(_('overall_discount'))
    latitude = models.FloatField(_('latitude'))
    longitude = models.FloatField(_('longitude'))
    delivery_time = models.IntegerField(_('delivery time'))
    communication = models.ForeignKey(Communication, verbose_name=_('communication'))
    package = models.ForeignKey(PartnerPackage, verbose_name=_('package'))
    open_hours = models.CharField(_('open_hours'), max_length=10)
    minimum_ord_val = models.IntegerField(_('minimum order value'))
    payment_method = models.ForeignKey(PaymentMethod, verbose_name=_('payment method'))
    employee = models.ForeignKey(Employee, verbose_name=_('employee'))
    contact_person = models.CharField(_('contact persoon'), max_length=50)    
    logo_path = models.ImageField(_('logo path'), upload_to="sport_icons", null=True)
    delivery_time_user = models.FloatField(_('delivery time user'))
    delivery_type = models.ForeignKey(DeliveryType, verbose_name=_('delivery type'))
    info = models.TextField(_('info'))
    active = models.BooleanField(_('active'), default=True)
    
    class Meta:
      verbose_name = _('Unit')
      verbose_name_plural = _('Units')

class Rating(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'))
    restaurant = models.ForeignKey(Unit, verbose_name=_('restaurant'))
    quality = models.SmallIntegerField(_('quality'))
    delivery_time = models.SmallIntegerField(_('delivery time'))
    feedback = models.TextField(_('feedback'))

    class Meta:
      verbose_name = _('Item')
      verbose_name_plural = _('Items')
