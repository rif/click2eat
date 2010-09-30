from django.contrib import admin
from menu import models

class SubCategoryInline(admin.TabularInline):
   model = models.SubCategoryTranslation
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

class VATAdmin(admin.ModelAdmin):
    list_display = ('value',)

class ItemGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"index": ("internal_name",)}
    list_display = ('internal_name', 'index', 'unit', 'exclusive', 'active')
    search_fields = ['internal_name']
    list_filter = ['unit']
    inlines = [ItemInline]

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('internal_name',)
    search_fields = ['internal_name']
    inlines = [SubCategoryInline]
    
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"index": ("internal_name",)}
    list_display = ('internal_name', 'index', 'unit', 'price', 'quantity', 'measurement_unit', 'vat', 'item_group', 'sub_category', 'special', 'active')
    search_fields = ['internal_name']
    list_filter = ['unit', 'special']
    inlines = [ItemTranslationInline]
    fieldsets = (
        (None, {
            'fields': ('internal_name', 'index', 'unit', ('price', 'vat'), ('quantity', 'measurement_unit'), 'item_group', 'sub_category', 'special')
        }),
        ('Discount', {
            'classes': ('collapse',),
            'fields': ('discount', 'discount_time_start', 'discount_time_end')
        }),
        ('Extra options', {
            'classes': ('collapse',),
            'fields': ('new_item_end_date', 'active')
        }),
    )

admin.site.register(models.Language)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.VAT, VATAdmin)
admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.ItemGroup, ItemGroupAdmin)
