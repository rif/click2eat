from django.contrib import admin
from bonus import models

class BonusAdmin(admin.ModelAdmin):
    list_display = ('user_name','order', 'amount')    
    
    def user_name(self, obj):
      return obj.order.user.get_full_name()
    user_name.short_description = 'Name'
    


admin.site.register(models.BonusTransaction, BonusAdmin)
