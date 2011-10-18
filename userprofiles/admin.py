from django.contrib import admin
from userprofiles import models

class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'additional_info', 'geolocated_address', 'latitude', 'longitude', 'geolocation_error', 'primary')
    list_filter = ['geolocation_error']
    search_fields = ['user__first_name', 'user__last_name', 'street', 'additional_info', 'geolocated_address']

    def save_model(self, request, obj, form, change):
        obj.perform_geolocation = False
        obj.save()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'phone', 'sex', 'birth_date','public')
    search_fields = ['__unicode__']
    list_filter = ['public']

admin.site.register(models.DeliveryAddress, DeliveryAddressAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
