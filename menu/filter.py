import django_filters
from menu.models import Item

class ItemFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(lookup_type='lt')
    quantity = django_filters.NumberFilter(lookup_type='gt')
    class Meta:
        model = Item
        order_by = ['price', 'quantity']
        fields = ['price', 'quantity', 'unit', 'promotion']
        
