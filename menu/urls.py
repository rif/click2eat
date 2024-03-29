from django.conf.urls.defaults import *
from menu import views
from menu.feeds import DailyMenuFeed


urlpatterns = patterns('',
                       url(r'^itemlist/$', views.item_list, name='item_list'),
                       url(r'^itemtaglist/(?P<tag>\w+-?\w+)$', views.item_tag_list, name='item_tag_list'),
                       url(r'^menulist/$', views.menu_list, name='menu_list'),
                       url(r'^dailymenus/$', views.daily_menus, name='daily_menus'),
                       url(r'^randommotd/$', views.random_motd, name='random_motd'),
                       url(r'^dailymenu/(?P<menu_id>\d+)/$', views.daily_menu, name='daily_menu'),
                       url(r'^feed/$', DailyMenuFeed(), name='daily_feed'),
                       )

