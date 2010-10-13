from django.conf.urls.defaults import *
from menu import views


urlpatterns = patterns('',
                       url(r'^itemlist/$', views.item_list, name='item_list'),
                       )
