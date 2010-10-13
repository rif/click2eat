import django_filters
from django.utils.translation import ugettext_lazy as _
from menu.models import Item

class ItemFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(lookup_type='lt')
    quantity = django_filters.NumberFilter(lookup_type='gt')

    def __init__(self, *args, **kwargs):
        super(ItemFilter, self).__init__(*args, **kwargs)
        self.filters['unit'].extra.update(
            {'empty_label': _('All restaurants')})
        self.filters['promotion'].extra.update(
            {'empty_label': _('All promotions')})

    class Meta:
        model = Item
        order_by = ['price', 'quantity']
        fields = ['price', 'quantity', 'unit', 'promotion']
            
