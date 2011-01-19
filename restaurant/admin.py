from django.contrib import admin
from restaurant import models
from menu.models import Item, ItemGroup, Topping
from restaurant.forms import UnitForm, FlatPageForm
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

class TinyMCEFlatPageAdmin(admin.ModelAdmin):
    form = FlatPageForm

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)

class CommunicationAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PartnerPackageAdmin(admin.ModelAdmin):
    list_display = ('unit','name', 'start_date', 'end_date', 'monthly_fee', 'rate', 'details', 'current')
    list_filter= ['unit']
    search_fields = ['name', 'details']

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'details')
    search_fields = ['name', 'details']

class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'require_address')
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

class ToppingInline(admin.TabularInline):
   model = Topping
   extra = 0
   min_num = 1

class IntervalInline(admin.TabularInline):
   model = models.Interval
   extra = 0
   min_num = 1

"""Currently not used because it was confiusing without intervals"""
class ScheduleInline(admin.TabularInline): 
   model = models.Schedule
   extra = 0
   min_num = 1

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('description', 'unit')
    list_filter= ['unit']
    search_fields = ['unit', 'description']
    inlines = [IntervalInline]

class UnitAdmin(admin.ModelAdmin):    
    form = UnitForm
    list_display = ('name', 'address', 'email', 'phone')
    search_fields = ['name', 'address']
    inlines = [ItemGroupInline, ItemInline, ToppingInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'address', ('email', 'phone', 'mobile'), 'logo_path')
        }),
        ('Location options', {
            'fields': (('latitude', 'longitude', 'delivery_range'), ('delivery_type', 'delivery_time'))
        }),
        ('Administration', {
            'fields': ('contact_person', 'admin_users', 'employee', 'communication')
        }),
        ('Payment info', {
            'fields': (('payment_method', 'currency'), 'overall_discount', 'minimum_ord_val')
        }),
        ('Other info', {
            'fields': ('tags', 'info', 'active')
        }),
    )
    
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'phone', 'start_date', 'end_date')
    search_fields = ['name', 'address']

admin.site.register(models.Employee, EmployeeAdmin)
admin.site.register(models.Unit, UnitAdmin)
admin.site.register(models.DeliveryType, DeliveryTypeAdmin)
admin.site.register(models.PaymentMethod,PaymentMethodAdmin)
admin.site.register(models.Communication, CommunicationAdmin)
admin.site.register(models.PartnerPackage, PartnerPackageAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
admin.site.register(models.Schedule, ScheduleAdmin)

