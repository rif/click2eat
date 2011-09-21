from django.conf.urls.defaults import *
from order import views
from order.models import Order

urlpatterns = patterns('',
                       url(r'^list/$', views.list, name='list'),
                       url(r'^list/(?P<unit_id>\d+)/$', views.list_unit, name='list_unit'),
                       url(r'^(?P<object_id>\d+)/$', views.limited_object_detail, {'queryset': Order.objects.all(), 'template_object_name': 'order'}, name='detail'),
                       url(r'^shop/(?P<cart_name>.+)/(?P<item_id>m?\d+_?\d*)/$', views.shop, name='shop'),
                       url(r'^decritem/(?P<cart_name>.+)/(?P<unit_id>\d+)/(?P<item_id>m?\d+_?\d*)/$', views.decr_item, name='decr-item'),
                       url(r'^incritem/(?P<cart_name>.+)/(?P<unit_id>\d+)/(?P<item_id>m?\d+_?\d*)/$', views.incr_item, name='incr-item'),
                       url(r'^shoppingcart/(?P<unit_id>\d+)/$', views.shopping_cart, name='shopping-cart'),
                       url(r'^sendorder/(?P<unit_id>\d+)/$', views.send_order, name='send-order'),
                       url(r'^addcart/$', views.add_cart, name='add-cart'),
                       url(r'^countdown/(?P<order_id>\d+)/$', views.timer, name='timer'),
                       url(r'^clone/(?P<order_id>\d+)/$', views.clone, name='clone'),
                       url(r'^feedback/(?P<order_id>\d+)/$', views.feedback, name='feedback'),
                       url(r'^hide/(?P<order_id>\d+)/$', views.hide, name='hide'),
                       url(r'^requireaddress/(?P<dt_id>\d+)/$', views.is_addres_required, name='require_address'),
                       )

urlpatterns += patterns('',
                       url(r'^restlist/(?P<unit_id>\d+)/$', views.restlist, name='restaurant_list'),
                       url(r'^restlistcsv/(?P<unit_id>\d+)/$', views.restlist_csv, name='restaurant_list_csv'),
                       url(r'^rl/(?P<unit_id>\d+)/$', views.restlist_ajax, name='restaurant_list_ajax'),
                       url(r'^rest/(?P<order_id>\d+)/$', views.restdetail, name='restaurant_detail'),
                       url(r'^delivered/(?P<order_id>\d+)/$', views.mark_delivered, name='restaurant_deliver'),
                       url(r'^confirm/(?P<order_id>\d+)/$', views.send_confiramtion_email, name='restaurant_confirm'),
                       )
