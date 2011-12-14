from django.conf.urls.defaults import *
from order import views
import shopping_service
from order.models import Order

urlpatterns = patterns('',
       url(r'^list/$', views.list, name='list'),
       url(r'^list/(?P<unit_id>\d+)/$', views.list_unit, name='list_unit'),
       url(r'^(?P<object_id>\d+)/$', views.limited_object_detail,
               {'queryset': Order.objects.all(), 'template_object_name': 'order'}, name='detail'),
       # uid!mMasterId-VarID_TopId
       url(r'^shop/(?P<unit_id>\d+)/(?P<cart_name>.+)/(?P<item_id>\d{13}!m?\d+-\d+_?\d*)/$', shopping_service.shop, name='shop'),
       url(r'^decritem/(?P<unit_id>\d+)/(?P<cart_name>.+)/(?P<item_id>\d{13}!m?\d+-\d+_?\d*)/$', shopping_service.decr_item,
           name='decr-item'),
       url(r'^incritem/(?P<unit_id>\d+)/(?P<cart_name>.+)/(?P<item_id>\d{13}!m?\d+-\d+_?\d*)/$', shopping_service.incr_item,
           name='incr-item'),
       url(r'^shoppingcart/(?P<unit_id>\d+)/$', shopping_service.shopping_cart, name='shopping-cart'),
       url(r'^confirmorder/(?P<unit_id>\d+)/$', views.confirm_order, name='confirm-order'),
       url(r'^sendorder/(?P<unit_id>\d+)/$', views.send_order, name='send-order'),
       url(r'^countdown/(?P<order_id>\d+)/$', views.timer, name='timer'),
       url(r'^clear/(?P<unit_id>\d+)/$', views.clear, name='clear'),
       url(r'^clone/(?P<order_id>\d+)/$', views.clone, name='clone'),
       url(r'^feedback/(?P<order_id>\d+)/$', views.feedback, name='feedback'),
       url(r'^hide/(?P<order_id>\d+)/$', views.hide, name='hide'),
       url(r'^requireaddress/(?P<dt_id>\d+)/$', views.is_addres_required, name='require_address'),
       )

urlpatterns += patterns('',
       url(r'^restlist/(?P<unit_id>\d+)/$', views.restlist, name='restaurant_list'),
       url(r'^restlistcsv/(?P<unit_id>\d+)/$', views.restlist_csv, name='restaurant_list_csv'),
       url(r'^rl/(?P<unit_id>\d+)/$', views.restlist_ajax, name='restaurant_list_ajax'),
       url(r'^rhl/(?P<unit_id>\d+)/$', views.restlist_history_ajax, name='restaurant_list_history_ajax'),
       url(r'^rest/(?P<order_id>\d+)/$', views.restdetail, name='restaurant_detail'),
       url(r'^delivered/(?P<order_id>\d+)/$', views.mark_delivered, name='restaurant_deliver'),
       )
