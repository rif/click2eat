from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from bonus import models

class BonusAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_name','order', 'amount')    
    
    def user_name(self, obj):
      return obj.order.user.get_full_name()
    user_name.short_description = _('From User')
    


admin.site.register(models.BonusTransaction, BonusAdmin)
