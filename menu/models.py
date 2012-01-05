from django.db import models
from multiling import MultilingualModel
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _
from annoying.functions import get_object_or_None
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

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
  index = models.FloatField(_('index'), help_text=_('Used for display order'))
  name_def = models.CharField(_('name'), max_length=50, help_text=_('The default name for this group'))
  unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))
  exclusive = models.BooleanField(_('exclusive'))
  active = models.BooleanField(_('active'), default=True)

  def get_name(self, lang=None):
    try:
      if lang == 'en' and self.name_en: return self.name_en
    except: pass
    return self.name_def 

  def __unicode__(self):
      return self.internal_name
  
  @staticmethod
  def autocomplete_search_fields():
      return ("id__iexact", "name_def__icontains", "internal_name__icontains", "unit__name__icontains")

  class Meta:
      translation = ItemGroupTranslation
      multilingual = ['name']
      ordering = ['unit__id','index']
      verbose_name = _('Item Group')
      verbose_name_plural = _('Item Groups')

class ToppingGroup(models.Model):
  internal_name = models.CharField(_('internal name'), max_length=50)
  unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))

  def __unicode__(self):
      return self.internal_name

  class Meta:
      ordering = ['unit__id']
      verbose_name = _('ToppingGroup')
      verbose_name_plural = _('ToppingGroup')

class MerchandiseCategoryGroup(models.Model):
  index = models.IntegerField(_('index'))
  name = models.CharField(_('name'), max_length=50)

  def __unicode__(self):
    return self.name

  class Meta:
    verbose_name = _('Merchandise Category Group')
    verbose_name_plural = _('Merchandise Category Groups')

class ItemTranslation(models.Model):
  language = models.ForeignKey('Language')
  name = models.CharField(_('name'), max_length=100)
  description = models.TextField(_('description'))
  model = models.ForeignKey('Item')

class Item(MultilingualModel):
  MU_CHOICES = (
      ('GR', 'g'),
      ('ML', 'ml'),
      ('PC', _('pieces')),
      ('CM', _('cm')),
      )
  internal_name = models.CharField(_('internal name'), max_length=70)
  index = models.FloatField(_('index'), help_text=_('Used for display order'))
  name_def = models.CharField(_('name'), max_length=70, help_text=_('The default name for this item'))
  description_def = models.CharField(_('description'), max_length=200, help_text=_('The default description for this item'))
  price = models.FloatField(_('price'))
  promotion = models.ForeignKey('Promotion', verbose_name=_('promotion'), null=True, blank=True)
  vat = models.ForeignKey(VAT, verbose_name=_('VAT'))
  quantity = models.IntegerField(_('quantity'))
  measurement_unit = models.CharField(_('MU'), max_length=2, choices=MU_CHOICES, default='GR', help_text=_('Measurement unit.'))
  item_group = models.ForeignKey(ItemGroup, verbose_name=_('item group'))
  added_date = models.DateField(_('added date'), auto_now_add=True, editable=False)
  toppings = models.ForeignKey(ToppingGroup, verbose_name=_('toppings'), null=True, blank=True)
  mcg = models.ForeignKey(MerchandiseCategoryGroup, verbose_name=('mcg'), null=True, blank=True)
  speciality = models.BooleanField(_('speciality'), help_text=_('speciality of the house'))
  fortune = models.BooleanField(_('fortune'), help_text=_('display in the weel of fortune'))
  free_pair = models.BooleanField(_('free pair'), help_text=_('given free with a similar more expensive pair'))
  image_path = models.ImageField(_('image path'), upload_to="item_images", null=True, blank=True)
  active = models.BooleanField(_('active'), default=True)

  tags = TaggableManager()

  def is_new(self):
        delta = date.today() - self.added_date
        return delta.days < 7

  def __unicode__(self):
      return self.name_def

  def get_name(self, lang=None, variation_id='0'):      
      n = self.name_def     
      try:
          if lang == 'en' and self.name_en: n = self.name_en
      except: pass
      if str(variation_id) != '0':
          variation = get_object_or_None(Variation, pk=variation_id)
          n += ' ' + variation.name      
      return n

  def get_description(self, lang=None):
    try:
      if lang == 'en' and self.description_en: return self.description_en
    except: pass
    return self.description_def    

  def get_id(self):
    return self.id

  def get_price(self, variation_id='0'):
      variation = None      
      if variation_id != '0':
          variation = get_object_or_None(Variation, pk=variation_id)
      if variation:  
          return round(variation.price,2) 
      return round(self.price,2)

  def has_promotion(self):
    return self.promotion and self.promotion.is_active()

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

  def quantity_with_mu(self):
      return '%d%s' % (self.quantity, self.get_measurement_unit_display())
  quantity_with_mu.short_description = _('Quantity')
  quantity_with_mu.admin_order_field = 'quantity'

  class Meta:
      ordering = ['index']
      translation = ItemTranslation
      multilingual = ['name', 'description']
      verbose_name = _('Item')
      verbose_name_plural = _('Items')

class Variation(models.Model):
    name = models.CharField(_('name'), max_length=100)
    item = models.ForeignKey('Item', verbose_name=_('item'))    
    price = models.FloatField(_('price'), default=1)
    active = models.BooleanField(_('active'), default=True)
    
    def __unicode__(self):
      return self.name 
    
    class Meta:
      ordering = ['name']        
      verbose_name = _('Variation')
      verbose_name_plural = _('Variation')

class ToppingTranslation(models.Model):
  language = models.ForeignKey('Language')
  name = models.CharField(_('name'), max_length=100)
  description = models.TextField(_('description'))
  model = models.ForeignKey('Topping')

class Topping(MultilingualModel):
  internal_name = models.CharField(_('internal name'), max_length=50)
  name_def = models.CharField(_('name'), max_length=50, help_text=_('The default name for this item'))
  description_def = models.CharField(_('description'), max_length=200, help_text=_('The default description for this item'))
  price = models.FloatField(_('price'))
  vat = models.ForeignKey(VAT, verbose_name=_('VAT'))
  quantity = models.IntegerField(_('quantity'))
  measurement_unit = models.CharField(_('MU'), max_length=2, choices=Item.MU_CHOICES, default='GR', help_text=_('Measurement unit.'))
  topping_group = models.ForeignKey(ToppingGroup, verbose_name=_('topping group'))
  added_date = models.DateField(_('added date'), auto_now_add=True, editable=False)
  mcg = models.ForeignKey(MerchandiseCategoryGroup, verbose_name=('mcg'), null=True, blank=True)
  active = models.BooleanField(_('active'), default=True)

  def get_name(self, lang=None, variation_id='0'):
    try:
      if lang == 'en' and self.name_en: return self.name_en
    except: pass
    return self.name_def 

  def get_description(self, lang=None):
    try:
      if lang == 'en' and self.description_en: return self.description_en
    except: pass
    return self.description_def 

  def get_id(self):
    return self.id

  def get_price(self, variation_id='0'):
      return self.price

  def __unicode__(self):
      return self.name_def

  class Meta:
    translation = ToppingTranslation
    multilingual = ['name', 'description']
    verbose_name = _('Topping')
    verbose_name_plural = _('Toppings')

class Promotion(models.Model):
    unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))
    name = models.CharField(_('name'), max_length=100)
    internal_name = models.CharField(_('internal name'), max_length=100)
    logo = models.ImageField(_('promotion logo'), upload_to="promotions_logos", null=True, blank=True)
    start_date = models.DateTimeField(_('start date'), null=True, blank=True)
    end_date = models.DateTimeField(_('end date'), null=True, blank=True)
    weekdays = models.CommaSeparatedIntegerField(_('weekdays'), max_length=13, null=True, blank=True, help_text=_('integer, comma separated, starting Monday=1 e.g. 1,2,3,4,5'))
    start_hour = models.CharField(_('start hour'), max_length=5, null=True, blank=True, help_text=_('e.g. 10:30'))
    end_hour = models.CharField(_('end hour'), max_length=5, null=True, blank=True, help_text=_('e.g. 15:00'))
    numer_of_items = models.IntegerField(_('numer of items'), default=1, help_text=_('Number of items involved. If there are 4+1 free then this value should be 5.'))
    total_sum_trigger = models.FloatField(_('total sum trigger'), default=0, help_text=_('Total order sum for which this promotion will become active'))
    procentage = models.IntegerField(_('procentage'), default=0, help_text=_('Percentage of the actual price'), null=True, blank=True)
    absolute_price = models.FloatField(_('absolute value'), default=0, help_text=_('Absolute price (fixed price)'), null=True, blank=True)

    def __unicode__(self):
        return self.name

    def is_active(self):
        return self._is_active(datetime.now())
    is_active.boolean = True

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
        if self.absolute_price:
            return self.absolute_price
        if self.procentage:
            return (old_price * (100-self.procentage))/100
        return 0


    class Meta:
        ordering = ['-start_date']
        verbose_name = _('Promotion')
        verbose_name_plural = _('Promotions')

class MenuOfTheDay(models.Model):
    unit = models.ForeignKey('restaurant.Unit', verbose_name=_('unit'))
    day = models.DateField(_('day'))
    name = models.CharField(_('name'), max_length=30)
    description = models.TextField(_('description'), max_length=50)
    price = models.FloatField(_('price'))

    @models.permalink
    def get_absolute_url(self):
      return ('menu:daily_menu', [str(self.id)])

    def get_name(self, lang=None, variation_id='0'):
      return self.name

    def get_description(self, lang=None):
      return self.description

    def get_id(self):
      return 'm%d' % self.id

    def get_price(self,variation_id='0'):
      return self.price

    class Meta:
        ordering = ['-day']
        verbose_name = _('Menu of the day')
        verbose_name_plural = _('Menu of the day')

class Import(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), editable=False, null=True, blank=True)
    import_date = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False)
    csv_file = models.FileField(upload_to='imports')

    def __unicode__(self):
        return 'Imported by %s at %s' % (self.user.get_full_name() or 'Admin', self.import_date.strftime('%d%B%Y %H:%M'))

    class Meta:
        ordering = ['-import_date']
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')
