from django.contrib import admin
from userprofiles import models

class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'additional_info', 'geolocated_address', 'primary')
    list_filter = ['geolocation_error', 'verified']
    search_fields = ['user__first_name', 'user__last_name', 'street', 'additional_info', 'geolocated_address']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'phone', 'sex', 'birth_date', 'newsletter')
    search_fields = ['__unicode__']
    list_filter = ['newsletter']

admin.site.register(models.DeliveryAddress, DeliveryAddressAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
