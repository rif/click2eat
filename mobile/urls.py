from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from mobile import views


urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name='mobile/home.html'), name='home'),
                       url(r'^accounts/login/$','django.contrib.auth.views.login', {'template_name':'mobile/login.html'},name='login'),
                       url(r'^accounts/logout/$','django.contrib.auth.views.logout',{'template_name':'mobile/logout.html'}, name='logout'),
                       url(r'^units/$', views.units, name='units'),
                       url(r'^menu/(?P<unit_id>\d+)/$', views.menu, name='menu'),
                       url(r'^search/$', views.search, name='search'),
                       url(r'^itemdetail/(?P<item_id>m?\d+)/$', views.item_detail, name='item-detail'),
                       url(r'^motd/$', views.motd, name='motd'),
                       url(r'^shop/(?P<item_id>m?\d+_?\d*)/$', views.shop, name='shop'),
                       url(r'^decritem/(?P<unit_id>\d+)/(?P<item_id>m?\d+_?\d*)/$', views.decr_item, name='decr-item'),
                       url(r'^incritem/(?P<unit_id>\d+)/(?P<item_id>m?\d+_?\d*)/$', views.incr_item, name='incr-item'),
                       url(r'^shoppingcart/(?P<unit_id>\d+)/$', views.shopping_cart, name='shopping-cart'),
                       url(r'^order/(?P<unit_id>\d+)/$', views.order, name='order'),
                       )
