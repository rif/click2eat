from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.shortcuts import get_object_or_404
from datetime import date
from django.db.models import Q
from menu.models import Item, MenuOfTheDay
from menu.filter import ItemFilter
from taggit.models import Tag

@render_to('menu/item_list.html')
def item_list(request):
    query = request.GET.get('q', '')
    results = Item.objects.all()
    if query:
        results = results.filter(Q(internal_name__icontains=query) | Q(name_def__icontains=query) | Q(description_def__icontains=query) | Q(tags__name__icontains=query) | Q(unit__name__icontains=query))
    f = ItemFilter(request.GET, queryset=results)
    return {'query': query, 'filter': f}

    
@login_required
@render_to('menu/daily_menu_list.html')
def daily_menus(request):    
    menus = MenuOfTheDay.objects.filter(day = date.today());
    return {'daily_menus': menus}

@render_to('menu/item_list.html')
def item_tag_list(request, tag):
    query = request.GET.get('q', '')
    results = Item.objects.filter(tags__name=tag)
    if query:
        results = results.filter(Q(internal_name__icontains=query) | Q(name_def__icontains=query) | Q(description_def__icontains=query) | Q(tags__name__icontains=query) | Q(unit__name__icontains=query))
    f = ItemFilter(request.GET, queryset=results)
    return {'query': query, 'filter': f}


@render_to('menu/menu_list.html')
def menu_list(request):
    tags = Item.tags.all()
    return {'tags': tags}

@render_to('menu/daily_menu.html')
def random_motd(request):    
    motds = MenuOfTheDay.objects.all()#.order_by('?')
    motd = motds[0] if len(motds) else None
    return locals()

@render_to('menu/daily_menu.html')
def daily_menu(request, menu_id):    
    motds = MenuOfTheDay.objects.all()#.order_by('?')
    motd = motds.get(pk=menu_id) if len(motds) else None
    return locals()
