from django.contrib import admin
from menu.models import *

class VATAdmin(admin.ModelAdmin):
    list_display = ('value',)

class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ('internal_name', 'unit', 'exclusive')
    search_fields = ['internal_name']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'description')
    search_fields = ['name', 'description']

class SpecialItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']

admin.site.register(SpecialItem, SpecialItemAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(VAT, VATAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(ItemGroup, ItemGroupAdmin)
