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

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',)
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
    fieldsets = (
        (None, {
            'fields': ('name', 'address', ('email', 'phone'), 'logo_path', 'open_hours', 'package')
        }),
        ('Location options', {
            'fields': ('unit_devlivery', ('latitude', 'longitude'), 'delivery_type', 'delivery_time')
        }),
        ('Administration', {
            'fields': ('contact_person', 'admin_users', 'employee', 'communication')
        }),
        ('Payment info', {
            'fields': (('payment_method', 'currency'), 'overall_discount', 'minimum_ord_val')
        }),
        ('Other info', {
            'classes': ('collapse',),
            'fields': ('info', 'active')
        }),
    )
    
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
admin.site.register(models.DeliveryArea, DeliveryAreaAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
