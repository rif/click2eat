from django.contrib import admin
from bonus import models

class BonusAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_user', 'money', 'received_date', 'used_date', 'used')
    list_filter = ['used', 'received_date', 'used_date']
    search_fields = ['user__first_name', 'user__last_name', 'from_user__first_name', 'from_user__last_name']


admin.site.register(models.Bonus, BonusAdmin)
