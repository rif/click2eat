from django.contrib import admin
from order.models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'unit', 'status', 'total_amount')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
