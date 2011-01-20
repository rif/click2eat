from django.conf.urls.defaults import *
from order import views
from order.models import Order

urlpatterns = patterns('',
                       url(r'^list/$', views.list, name='list'),
                       url(r'^list/(?P<unit_id>\d+)/$', views.list_unit, name='list_unit'),
                       url(r'^(?P<object_id>\d+)/$', views.limited_object_detail, {'queryset': Order.objects.all(), 'template_object_name': 'order'}, name='detail'),
                       url(r'^add_item/(?P<item_id>\d+)/(?P<cart_name>.+)/$', views.add_item, name='add_item'),
                       url(r'^add_topping/(?P<master_id>\d+)/(?P<item_id>\d+)/(?P<cart_name>.+)/$', views.add_topping, name='add_topping'),
                       url(r'^add_motd/(?P<item_id>\d+)/(?P<cart_name>.+)/$', views.add_menu_of_the_day, name='add_motd'),
                       url(r'^remove_item/(?P<item_id>\d+)/$', views.remove_item, name='remove_item'),
                       url(r'^get_current/(?P<unit_id>\d+)/$', views.get_current_order, name='get_current'),
                       url(r'^send/(?P<unit_id>\d+)/$', views.send, name='send'),
                       url(r'^get_total_amount/(?P<order_id>\d+)/$', views.get_total_amount, name='get_total_amount'),
                       url(r'^get_subtotal/(?P<unit_id>\d+)/(?P<cart_name>.+)/$', views.get_subtotal, name='get_subtotal'),
                       url(r'^add_cart/(?P<order_id>\d+)/$', views.add_cart, name='add_cart'),
                       url(r'^get_cart/(?P<order_id>\d+)/(?P<cartname>.+)/$', views.get_cart, name='get_cart'),
                       url(r'^countdown/(?P<order_id>\d+)/$', views.timer, name='timer'),
                       url(r'^clone/(?P<order_id>\d+)/$', views.clone, name='clone'),
                       url(r'^feedback/(?P<order_id>\d+)/$', views.feedback, name='feedback'),
                       url(r'^getavailabletoppings/(?P<unit_id>\d+)/$', views.get_available_toppings, name='available_toppings'),
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
