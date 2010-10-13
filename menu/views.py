from annoying.decorators import render_to
from menu.models import Item
from menu.filter import ItemFilter

@render_to('menu/item_list.html')
def item_list(request):
    f = ItemFilter(request.GET, queryset=Item.objects.all())
    return {'filter': f}
