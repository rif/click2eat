import django_filters
from menu.models import Item

class ItemFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(lookup_type='lt')
    class Meta:
        model = Item
        order_by = ['price', 'unit', 'name_ro']
        fields = ['price', 'item_group', 'tags']
        
