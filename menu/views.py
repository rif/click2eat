from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from datetime import date
from django.db.models import Q
from menu.models import Item, MenuOfTheDay
from menu.filter import ItemFilter

@render_to('menu/item_list.html')
def item_list(request):
    query = request.GET.get('q', '')
    results = Item.objects.filter(active=True).select_related('item_group__unit','promotion__unit').order_by('name_def')
    if query:
        results = results.filter(Q(internal_name__icontains=query) | Q(name_def__icontains=query) | Q(description_def__icontains=query) | Q(tags__name__icontains=query) | Q(item_group__unit__name__icontains=query) | Q(mcg__name__icontains=query)).distinct()
    f = ItemFilter(request.GET, queryset=results)
    return {'query': query, 'filter': f}


@login_required
@render_to('menu/daily_menu_list.html')
def daily_menus(request):
    menus = MenuOfTheDay.objects.filter(day = date.today());
    return {'daily_menus': menus}

@render_to('menu/item_list.html')
def item_tag_list(request, tag):
    results = Item.objects.filter(active=True).select_related('item_group__unit', 'promotion__unit').filter(Q(tags__slug__icontains=tag)).order_by('name_def').distinct()
    f = ItemFilter(request.GET, queryset=results)
    return {'tag': tag, 'filter': f}


@render_to('menu/menu_list.html')
def menu_list(request):
    tags = Item.tags.all()
    return {'tags': tags}

@render_to('menu/daily_menu.html')
def random_motd(request):
    motds = MenuOfTheDay.objects.filter(day=date.today())#.order_by('?')
    motd = motds[0] if motds.exists() else None
    return locals()

@render_to('menu/daily_menu.html')
def daily_menu(request, menu_id):
    motds = MenuOfTheDay.objects.filter(day=date.today())    
    motd = motds.filter(pk=menu_id) if motds.exists() else None
    motd = motd[0] if motd and motd.exists() else None
    return locals()
