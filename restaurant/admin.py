from django.contrib import admin
from restaurant import models
from django import forms
from menu.models import Item, ItemGroup, Topping
from ckeditor.widgets import CKEditorWidget

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

class ItemAdminForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'info', 'address', 'package' , 'email', 'address', 'phone', 'mobile', 'email',
                  'logo_path', 'contact_person', 'admin_users', 'employee', 'communication', 'latitude',
                  'longitude', 'delivery_range', 'delivery_type', 'delivery_time', 'payment_method',
                  'currency', 'overall_discount', 'minimum_ord_val', 'tags', 'info', 'active')
        widgets = {
            'info': CKEditorWidget(),
        }

class UnitAdmin(admin.ModelAdmin):    
    form = ItemAdminForm
    list_display = ('name', 'address', 'package', 'email', 'phone')
    search_fields = ['name', 'address']
    inlines = [ItemGroupInline, ItemInline, ToppingInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'address', ('email', 'phone', 'mobile'), 'logo_path', 'package')
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

