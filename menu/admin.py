from django.contrib import admin
from menu import models

class ItemTranslationInline(admin.StackedInline):
   model = models.ItemTranslation
   extra = 1
   min_num = 1

class VATAdmin(admin.ModelAdmin):
    list_display = ('value',)

class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ('internal_name', 'unit', 'exclusive')
    search_fields = ['internal_name']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class ItemAdmin(admin.ModelAdmin):
    list_display = ('unit',)
    #search_fields = ['name', 'description']
    inlines = [ItemTranslationInline]

class SpecialItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']

admin.site.register(models.Language)
admin.site.register(models.SpecialItem, SpecialItemAdmin)
admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.VAT, VATAdmin)
admin.site.register(models.SubCategory, SubCategoryAdmin)
admin.site.register(models.ItemGroup, ItemGroupAdmin)
