from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from datetime import date
from django.db.models import Q
from menu.models import Item, MenuOfTheDay
from menu.filter import ItemFilter

@login_required
@render_to('menu/item_list.html')
def item_list(request):
    query = request.GET.get('q', '')
    results = Item.objects.all()
    if query:
        results = results.filter(Q(internal_name__icontains=query) | Q(name_def__icontains=query) | Q(description_def__icontains=query) | Q(tags__name__icontains=query) | Q(unit__name__icontains=query))
    f = ItemFilter(request.GET, queryset=results)
    return {'query': query, 'filter': f}

    
@login_required
@render_to('menu/daily_menu.html')
def daily_menu(request):    
    menues = MenuOfTheDay.objects.filter(day = date.today());
    return {'daily_menues': menues}
