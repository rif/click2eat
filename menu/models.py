from django.db import models
from multiling import MultilingualModel
from django.utils.translation import ugettext_lazy as _

class Language(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.name

class VAT(models.Model):
  value = models.FloatField()
  
  def __unicode__(self):
      return "VAT: " + str(self.value)
  
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
