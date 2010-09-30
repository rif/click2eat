from django.contrib import admin
from restaurant import models
from menu.models import Item, ItemGroup 

class DeliveryAreaAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
class CommunicationAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PartnerPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')
    search_fields = ['name', 'details']
    prepopulated_fields = {"slug": ("name",)}

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')
    search_fields = ['name', 'details']

class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ['name']

class ItemInline(admin.TabularInline):
   model = Item
   extra = 0
   min_num = 1
   
class ItemGroupInline(admin.TabularInline):
   model = ItemGroup
   extra = 0
   min_num = 1

class UnitAdmin(admin.ModelAdmin):    
    list_display = ('name', 'address', 'package', 'email', 'phone')
    search_fields = ['name', 'address']
    inlines = [ItemGroupInline, ItemInline]
    
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'phone', 'start_date', 'end_date')
    search_fields = ['name', 'address']

class RatingAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'quality', 'delivery_time', 'feedback')
    search_fields = ['user', 'restaurant', 'feedback']

admin.site.register(models.Rating, RatingAdmin)
admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Unit, UnitAdmin)
admin.site.register(models.DeliveryType, DeliveryTypeAdmin)
admin.site.register(models.PaymentMethod,PaymentMethodAdmin)
admin.site.register(models.Communication, CommunicationAdmin)
admin.site.register(models.PartnerPackage, PartnerPackageAdmin)
admin.site.register(models.DeliveryArea, DeliveryAreaAdmin )


