from annoying.decorators import render_to
from django.db.models import Q
from menu.models import Item
from menu.filter import ItemFilter

@render_to('menu/item_list.html')
def item_list(request):
    query = request.GET.get('q', '')
    results = Item.objects.all()
    if query:
        results = results.filter(Q(internal_name__icontains=query) | Q(tags__name__icontains=query) | Q(unit__name__icontains=query))
    f = ItemFilter(request.GET, queryset=results)
    return {'query': query, 'filter': f}
