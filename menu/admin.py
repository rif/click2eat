from django.contrib import admin
from menu import models

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
    list_display = ('internal_name', 'index', 'unit', 'exclusive', 'active')
    search_fields = ['internal_name']
    list_filter = ['unit']
    inlines = [ItemInline]
    inlines = [ItemGroupInline]

class ToppingGroupAdmin(admin.ModelAdmin):
    list_display = ('internal_name',)
    search_fields = ['internal_name']
    inlines = [ToppingInline]
    
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"index": ("internal_name",)}
    list_display = ('internal_name', 'index', 'unit', 'price', 'quantity', 'measurement_unit', 'vat', 'item_group', 'toppings', 'active')
    search_fields = ['internal_name']
    list_filter = ['unit']
    inlines = [ItemTranslationInline]
    fieldsets = (
        (None, {
            'fields': ('internal_name', 'index', 'unit', ('price', 'vat'), ('quantity', 'measurement_unit'), 'item_group', 'toppings')
        }),
        ('Extra options', {
            'fields': ('new_item_end_date', 'active')
        }),
    )

class ToppingAdmin(admin.ModelAdmin):
    prepopulated_fields = {"index": ("internal_name",)}
    list_display = ('internal_name', 'index', 'unit', 'price', 'quantity', 'measurement_unit', 'vat', 'active')
    search_fields = ['internal_name']
    list_filter = ['unit']
    inlines = [ItemTranslationInline]
    fieldsets = (
        (None, {
            'fields': ('internal_name', 'index', 'unit', ('price', 'vat'), ('quantity', 'measurement_unit'), 'topping_groups')
        }),
        ('Extra options', {
            'fields': ('new_item_end_date', 'active')
        }),
    )

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'value', 'start_date', 'end_date', 'weekdays', 'start_hour', 'end_hour')
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

admin.site.register(models.Language)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.VAT, VATAdmin)
admin.site.register(models.ItemGroup, ItemGroupAdmin)
admin.site.register(models.Topping, ToppingAdmin)
admin.site.register(models.ToppingGroup, ToppingGroupAdmin)
admin.site.register(models.Promotion, PromotionAdmin)
