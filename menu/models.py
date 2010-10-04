from django.db import models
from multiling import MultilingualModel
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

class Language(models.Model):
    code = models.CharField(_('code'), max_length=5)
    name = models.CharField(_('name'), max_length=16)
    
    def __unicode__(self):
        return self.name

class VAT(models.Model):
  name = models.CharField(_('name'), max_length=20)
  value = models.FloatField(_('value'))
  
  def __unicode__(self):
      return self.name
  
  class Meta:
      verbose_name = _('VAT')
      verbose_name_plural = _('VAT')
      
class ItemGroupTranslation(models.Model):
  language = models.ForeignKey('Language')
  name = models.CharField(_('name'), max_length=100)
  model = models.ForeignKey('ItemGroup')

class ItemGroup(MultilingualModel):
  internal_name = models.CharField(_('internal name'), max_length=50)
  index = models.CharField(_('index'), max_length=50, help_text=_('Used for display order'))
  unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))
  exclusive = models.BooleanField(_('exclusive'))
  active = models.BooleanField(_('active'), default=True)
  
  def __unicode__(self):
      return self.internal_name

  class Meta:
      translation = ItemGroupTranslation
      multilingual = ['name']
      ordering = ['index']
      verbose_name = _('Item Group')
      verbose_name_plural = _('Item Groups')

class ToppingGroup(models.Model):
  internal_name = models.CharField(_('internal name'), max_length=50)
  
  def __unicode__(self):
      return self.internal_name

  class Meta:
      verbose_name = _('ToppingGroup')
      verbose_name_plural = _('ToppingGroup')

class ItemTranslation(models.Model):
  language = models.ForeignKey('Language')
  name = models.CharField(_('name'), max_length=100)
  description = models.TextField(_('description'))
  model = models.ForeignKey('Item')

class Item(MultilingualModel):
  MU_CHOICES = (
      ('GR', 'g'),
      ('ML', 'ml'),
      )
  internal_name = models.CharField(_('internal name'), max_length=50)
  index = models.CharField(_('index'), max_length=50, help_text=_('Used for display order'))
  unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))
  price = models.FloatField(_('price'))
  quantity = models.IntegerField(_('quantity'))
  promotion = models.ForeignKey('Promotion', verbose_name=_('promotion'), null=True, blank=True)
  measurement_unit = models.CharField(_('MU'), max_length=2, choices=MU_CHOICES, default='GR', help_text=_('Measurement unit.')) 
  vat = models.ForeignKey(VAT, verbose_name=_('VAT'))
  item_group = models.ForeignKey(ItemGroup, verbose_name=_('item group'), null=True, blank=True)
  new_item_end_date = models.DateField(_('new item end date'), null=True, blank=True)
  toppings = models.ForeignKey(ToppingGroup, verbose_name=_('toppings'), null=True, blank=True)
  active = models.BooleanField(_('active'), default=True)
  
  def __unicode__(self):
      return self.internal_name
  
  class Meta:
      ordering = ['index']
      translation = ItemTranslation
      multilingual = ['name', 'description']
      verbose_name = _('Item')
      verbose_name_plural = _('Items')

class Topping(Item):
    topping_groups = models.ManyToManyField(ToppingGroup)
    
    class Meta:
      ordering = ['index']
      translation = ItemTranslation
      multilingual = ['name', 'description']
      verbose_name = _('Topping')
      verbose_name_plural = _('Toppings')
      
class Promotion(models.Model):
    unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))
    name = models.CharField(_('name'), max_length=50)
    start_date = models.DateTimeField(_('start date'), null=True, blank=True)
    end_date = models.DateTimeField(_('end date'), null=True, blank=True)
    weekdays = models.CommaSeparatedIntegerField(_('weekdays'), max_length=13, null=True, blank=True, help_text=_('integer, comma separated, starting Monday=1 e.g. 1,2,3,4,5'))
    start_hour = models.CharField(_('start hour'), max_length=5, null=True, blank=True, help_text=_('e.g. 10:30'))
    end_hour = models.CharField(_('end hour'), max_length=5, null=True, blank=True, help_text=_('e.g. 15:00'))
    value = models.IntegerField(_('value'), default=0, help_text=_('Percentage'))
    
    def __unicode__(self):
        return self.name
    
    def is_active(self):
        now = datetime.now()
        weekday = now.isoweekday()
        if start_date and now < start_date:
            return False
        if end_date and now > end_date:
            return False
        if str(weekday) not in weekdays:
            return False
        return True
    
    def get_new_price(self, old_price):
        return (old * (100-self.value))/100
        
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = _('Promotion')
        verbose_name_plural = _('Promotions')
