from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from menu import models
from menu.forms import MenuOfTheDayForm

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
      unit = self.cleaned_data['unit']
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
            'fields': ('internal_name', 'index', ('name_def', 'description_def'), 'unit', ('price', 'promotion','vat'), ('quantity', 'measurement_unit'), 'item_group', 'toppings')
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


admin.site.register(models.Language)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.VAT, VATAdmin)
admin.site.register(models.ItemGroup, ItemGroupAdmin)
admin.site.register(models.Topping, ToppingAdmin)
admin.site.register(models.ToppingGroup, ToppingGroupAdmin)
admin.site.register(models.Promotion, PromotionAdmin)
admin.site.register(models.MenuOfTheDay, MenuOfTheDayAdmin)
