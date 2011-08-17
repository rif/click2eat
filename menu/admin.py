from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from menu import models
from menu.forms import MenuOfTheDayForm
from annoying.functions import get_object_or_None
from restaurant.models import Unit
from django.contrib import messages
import csv

class ItemGroupInline(admin.TabularInline):
   model = models.ItemGroupTranslation
   extra = 0
   min_num = 1

class ItemTranslationInline(admin.TabularInline):
   model = models.ItemTranslation
   extra = 0
   min_num = 1

class ItemInline(admin.TabularInline):
   model = models.Item
   extra = 0
   min_num = 1

class ToppingInline(admin.TabularInline):
   model = models.Topping
   extra = 0
   min_num = 1

class VATAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')

class ItemGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"index": ("internal_name",)}
    list_display = ('internal_name', 'name_def', 'index', 'unit', 'exclusive', 'active')
    search_fields = ['internal_name']
    list_filter = ['unit']
    inlines = [ItemGroupInline, ItemInline]

class ToppingGroupAdmin(admin.ModelAdmin):
    list_display = ('internal_name',)
    search_fields = ['internal_name']
    inlines = [ToppingInline]

class ItemForm(forms.ModelForm):
    class Meta:
      model = models.Item

    def clean(self):
      if self.cleaned_data.has_key('item_group'):
        unit = self.cleaned_data['unit']
      else:
        return self.cleaned_data
      group = None
      if self.cleaned_data.has_key('item_group'):
        group = self.cleaned_data['item_group']
      if group and (unit != group.unit):
        raise forms.ValidationError(_("Item's unit differs form item's group unit."))
      return self.cleaned_data

class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    prepopulated_fields = {"index": ("internal_name",)}
    list_display = ('internal_name', 'index','name_def', 'description_def', 'unit', 'get_price', 'promotion', 'quantity_with_mu', 'vat', 'item_group', 'toppings', 'active')
    search_fields = ['internal_name', 'name_def', 'description_def']
    list_editable = ['promotion']
    list_filter = ['unit']
    inlines = [ItemTranslationInline]
    actions = ['clone_objects']
    fieldsets = (
        (None, {
            'fields': ('internal_name', 'index', ('name_def', 'description_def'), 'unit', ('price', 'promotion','vat'), ('quantity', 'measurement_unit'), ('item_group', 'toppings', 'mcg'))
        }),
        ('Extra options', {
            'fields': ('tags', 'active')
        }),
    )

    def clone_objects(self, request, queryset):
        for object in queryset.iterator():
            object.clone()
        rows_updated = queryset.count()
        if rows_updated == 1:
            message_bit = _("1 item was")
        else:
            message_bit = _("%s items were") % rows_updated
        self.message_user(request, _("%s successfully cloned.") % message_bit)
    clone_objects.short_description = _('Clone selected items')


class ToppingAdmin(admin.ModelAdmin):
    prepopulated_fields = {"index": ("internal_name",)}
    list_display = ('internal_name', 'index', 'unit', 'get_price', 'quantity', 'measurement_unit', 'vat', 'active')
    search_fields = ['internal_name']
    list_filter = ['unit']
    inlines = [ItemTranslationInline]
    fieldsets = (
        (None, {
            'fields': ('internal_name', 'index', 'unit', ('price', 'promotion', 'vat'), ('quantity', 'measurement_unit'), 'topping_groups')
        }),
        ('Extra options', {
            'fields': ('tags', 'active')
        }),
    )

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'value', 'start_date', 'end_date', 'weekdays', 'start_hour', 'end_hour', 'is_active')
    list_filter = ['unit', 'start_date']
    search_fields = ['internal_name']
    fieldsets = (
        (None, {
            'fields': ('name', 'unit', 'value')
        }),
        ('Time option', {
            'fields': (('start_date', 'end_date'), 'weekdays', ('start_hour', 'end_hour'))
        }),
    )

class MenuOfTheDayAdmin(admin.ModelAdmin):
   form = MenuOfTheDayForm
   list_display = ('unit', 'day', 'price')
   list_filter = ['unit', 'day']
   search_fields = ['items__name_def']

class MerchandiseCategoryGroupAdmin(admin.ModelAdmin):
   search_fields = ['name']

class ImportAdmin(admin.ModelAdmin):
   def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

        menu_file = csv.reader(open(obj.csv_file.path), delimiter=',', quotechar='"')
        last_group = None
        index = 0
        header_row = True
        for row in menu_file:
           if header_row:
              header_row = False
              continue
           unit_name = row[4]
           unit = get_object_or_None(Unit, name=unit_name)
           if not unit:
              messages.add_message(request, messages.ERROR, _('There is no unit with name %s defined') % unit_name)
              return
           if index == 0 and unit.itemgroup_set.count():
              messages.add_message(request, messages.ERROR, _('This unit allready has menu items'))
              return
           group_name = row[8]
           if not last_group or last_group.name_def != group_name:
              index += 1
              last_group = models.ItemGroup.objects.get_or_create(internal_name=group_name, index=str(index), name_def=group_name, unit=unit)[0]
           models.Item.objects.create(internal_name=row[0], index=row[1], name_def=row[2], description_def=row[3], unit=unit, item_group=last_group, price=row[5], quantity=row[6], measurement_unit=row[7], vat_id=1) #the VAT is hardcoded to first one :(

admin.site.register(models.Language)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.VAT, VATAdmin)
admin.site.register(models.ItemGroup, ItemGroupAdmin)
admin.site.register(models.Topping, ToppingAdmin)
admin.site.register(models.ToppingGroup, ToppingGroupAdmin)
admin.site.register(models.Promotion, PromotionAdmin)
admin.site.register(models.MenuOfTheDay, MenuOfTheDayAdmin)
admin.site.register(models.MerchandiseCategoryGroup, MerchandiseCategoryGroupAdmin)
admin.site.register(models.Import, ImportAdmin)
