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

class ItemGroup(models.Model):
  internal_name = models.CharField(_('internal name'), max_length=50)
  unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))
  exclusive = models.BooleanField(_('exclusive'))
  active = models.BooleanField(_('active'), default=True)
  
  def __unicode__(self):
      return self.internal_name

  class Meta:
      verbose_name = _('Item Group')
      verbose_name_plural = _('Item Groups')

class SubCategoryTranslation(models.Model):
  language = models.ForeignKey('Language')
  name = models.CharField(_('name'), max_length=100)
  model = models.ForeignKey('SubCategory')

      
class SubCategory(MultilingualModel):
  internal_name = models.CharField(_('name'), max_length=50)
  
  def __unicode__(self):
      return self.internal_name

  class Meta:
      translation = SubCategoryTranslation
      multilingual = ['name']
      verbose_name = _('Subcategory')
      verbose_name_plural = _('Subcategories')

class ItemTranslation(models.Model):
  language = models.ForeignKey('Language')
  name = models.CharField(_('name'), max_length=100)
  description = models.TextField(_('description'))
  model = models.ForeignKey('Item')

class Item(MultilingualModel):
  internal_name = models.CharField(_('internal name'), max_length=50)
  unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))
  price = models.FloatField(_('price'))
  vat = models.ForeignKey(VAT, verbose_name=_('VAT'))
  discount = models.IntegerField(_('discount'), null=True, blank=True)
  discount_time_start = models.DateTimeField(_('discount time start'), null=True, blank=True)
  discount_time_end = models.DateTimeField(_('discount time end'), null=True, blank=True)
  item_group = models.ForeignKey(ItemGroup, verbose_name=_('item group'), null=True, blank=True)
  new_item_end_date = models.DateField(_('new item end date'), null=True, blank=True)
  sub_category = models.ForeignKey(SubCategory, verbose_name=_('sub category'))
  special = models.BooleanField(_('special'))
  active = models.BooleanField(_('active'), default=True)
  
  def __unicode__(self):
      return self.internal_name
  
  class Meta:
      translation = ItemTranslation
      multilingual = ['name', 'description']
      verbose_name = _('Item')
      verbose_name_plural = _('Items')


class SpecialItemTranslation(models.Model):
  language = models.ForeignKey('Language')
  name = models.CharField(_('name'), max_length=100)
  description = models.TextField(_('description'))
  model = models.ForeignKey('SpecialItem')

class SpecialItem(MultilingualModel):
  internal_name = models.CharField(_('internal name'), max_length=50)
  price = models.FloatField(_('price'),)
  vat = models.ForeignKey(VAT, verbose_name=_('VAT'))
  time_start = models.DateTimeField(_('time start'))
  time_end = models.DateTimeField(_('time end'))
  item_group = models.ForeignKey(ItemGroup, verbose_name=_('item group'))
  active = models.BooleanField(_('active'), default=True)
  
  def __unicode__(self):
      return self.internal_name
  
  class Meta:
      translation = SpecialItemTranslation
      multilingual = ['name', 'description']
      verbose_name = _('Special item')
      verbose_name_plural = _('Special items')
