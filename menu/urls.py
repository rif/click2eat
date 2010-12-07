from django.conf.urls.defaults import *
from menu import views
from menu.feeds import DailyMenuFeed


urlpatterns = patterns('',
                       url(r'^itemlist/$', views.item_list, name='item_list'),
                       url(r'^dailymenues/$', views.daily_menues, name='daily_menues'),
                       url(r'^dailymenu/(?P<menu_id>\d+)/$', views.daily_menu, name='daily_menu'),
                       url(r'^feed/$', DailyMenuFeed()),
                       )
