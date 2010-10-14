from django.db import models
from multiling import MultilingualModel
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

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
  added_date = models.DateField(_('added date'), auto_now_add=True, editable=False)
  toppings = models.ForeignKey(ToppingGroup, verbose_name=_('toppings'), null=True, blank=True)
  active = models.BooleanField(_('active'), default=True)

  tags = TaggableManager()
  
  def is_new(self):
        delta = date.today() - self.added_date
        return delta.days < 7

  def __unicode__(self):
      return self.internal_name

  def get_price(self):
      if self.promotion:
          return self.promotion.get_new_price(self.price)
      return self.price

  def clone(self):
      ci = Item()
      ci.internal_name = self.internal_name
      ci.index = self.index
      ci.unit = self.unit
      ci.price = self.price
      ci.quantity = self.quantity
      ci.promotion = self.promotion
      ci.measurement_unit = self.measurement_unit
      ci.vat = self.vat
      ci.item_group = self.item_group
      ci.new_item_end_date = self.new_item_end_date
      ci.toppings = self.toppings
      ci.active = self.active
      ci.save()
      return ci
  
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
        return self._is_active(datetime.now())
    
    def _is_active(self, check_date):
        now = check_date
        weekday = now.isoweekday()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        if self.weekdays and str(weekday) not in self.weekdays:
            return False
        if self.start_hour:
            starth = datetime.strptime(now.strftime("%d-%m-%Y ") + self.start_hour, "%d-%m-%Y %H:%M")
            if now < starth:
                return False
        if self.end_hour:
            endh = datetime.strptime(now.strftime("%d-%m-%Y ") + self.end_hour, "%d-%m-%Y %H:%M")
            if now > endh:
                return False
        return True
    
    def get_new_price(self, old_price):
        return (old_price * (100-self.value))/100
        
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = _('Promotion')
        verbose_name_plural = _('Promotions')
