from django.contrib import admin
from order.models import Order, OrderItem, Rating

class OrderItemInline(admin.TabularInline):
   model = OrderItem
   extra = 0
   min_num = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'unit', 'status', 'creation_date', 'total_amount', 'employee', 'additional_info')
    list_filter = ('status', 'creation_date')
    inlines=[OrderItemInline]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'quality', 'delivery_time', 'feedback')
    search_fields = ['feedback']

admin.site.register(Rating, RatingAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
