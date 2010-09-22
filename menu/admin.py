from django.contrib import admin
from menu import models

class SubCategoryInline(admin.TabularInline):
   model = models.SubCategoryTranslation
   extra = 1
   min_num = 1

class ItemTranslationInline(admin.TabularInline):
   model = models.ItemTranslation
   extra = 1
   min_num = 1

class SpecialItemTranslationInline(admin.TabularInline):
   model = models.SpecialItemTranslation
   extra = 1
   min_num = 1

class ItemInline(admin.TabularInline):
   model = models.Item
   extra = 1
   min_num = 1

class VATAdmin(admin.ModelAdmin):
    list_display = ('value',)

class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ('internal_name', 'unit', 'exclusive')
    search_fields = ['internal_name']
    inlines = [ItemInline]

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('internal_name',)
    search_fields = ['internal_name']
    inlines = [SubCategoryInline]
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('internal_name',)
    search_fields = ['internal_name']
    inlines = [ItemTranslationInline]

class SpecialItemAdmin(admin.ModelAdmin):
    list_display = ('internal_name',)
    search_fields = ['internal_name']
    inlines = [SpecialItemTranslationInline]

admin.site.register(models.Language)
admin.site.register(models.SpecialItem, SpecialItemAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.VAT, VATAdmin)
admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.ItemGroup, ItemGroupAdmin)
