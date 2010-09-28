from django.contrib import admin
from restaurant.models import *

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

class UnitAdmin(admin.ModelAdmin):    
    list_display = ('name', 'address', 'package', 'email', 'phone')
    search_fields = ['name', 'address']
    
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'phone', 'start_date', 'end_date')
    search_fields = ['name', 'address']

class RatingAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'quality', 'delivery_time', 'feedback')
    search_fields = ['user', 'restaurant', 'feedback']

admin.site.register(Rating, RatingAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(DeliveryType, DeliveryTypeAdmin)
admin.site.register(PaymentMethod,PaymentMethodAdmin)
admin.site.register(Communication, CommunicationAdmin)
admin.site.register(PartnerPackage, PartnerPackageAdmin)
admin.site.register(DeliveryArea, DeliveryAreaAdmin )


