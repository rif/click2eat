from django.contrib import admin
from order.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
   model = OrderItem
   extra = 0
   min_num = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'unit', 'status', 'creation_date', 'total_amount', 'additional_info')
    list_filter = ('status', 'creation_date')
    inlines=[OrderItemInline]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
