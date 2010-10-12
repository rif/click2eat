from django.conf.urls.defaults import *
from order import views
from order.models import Order

urlpatterns = patterns('',
                       url(r'^list/$', views.list, name='list'),
                       url(r'^list/(?P<unit_id>\d+)/$', views.list_unit, name='list_unit'),
                       url(r'^(?P<object_id>\d+)/$', views.limited_object_detail, {'queryset': Order.objects.all(), 'template_object_name': 'order'}, name='detail'),
                       url(r'^add_item/(?P<item_id>\d+)/(?P<cart_name>.+)/$', views.add_item, name='add_item'),
                       url(r'^remove_item/(?P<item_id>\d+)/$', views.remove_item, name='remove_item'),
                       url(r'^get_current/(?P<unit_id>\d+)/$', views.get_current_order, name='get_current'),
                       url(r'^send/(?P<unit_id>\d+)/$', views.send, name='send'),
                       url(r'^get_total_amount/(?P<order_id>\d+)/$', views.get_total_amount, name='get_total_amount'),
                       url(r'^get_subtotal/(?P<unit_id>\d+)/(?P<cart_name>.+)/$', views.get_subtotal, name='get_subtotal'),
                       url(r'^add_cart/(?P<unit_id>\d+)/$', views.add_cart, name='add_cart'),
                       url(r'^countdown/(?P<order_id>\d+)/$', views.timer, name='timer'),
                       url(r'^clone/(?P<order_id>\d+)/$', views.clone, name='clone'),
                       url(r'^feedback/(?P<order_id>\d+)/$', views.feedback, name='feedback'),
                       url(r'^notrated/$', views.not_rated, name='not_rated'),
                       )

urlpatterns += patterns('',
                       url(r'^restlist/(?P<unit_id>\d+)/$', views.restlist, name='restaurant_list'),
                       url(r'^restlistcsv/(?P<unit_id>\d+)/$', views.restlist_csv, name='restaurant_list_csv'),
                       url(r'^rl/(?P<unit_id>\d+)/$', views.restlist_ajax, name='restaurant_list_ajax'),
                       url(r'^rest/(?P<order_id>\d+)/$', views.restdetail, name='restaurant_detail'),
                       url(r'^delivered/(?P<order_id>\d+)/$', views.mark_delivered, name='restaurant_deliver'),
                       url(r'^confirm/(?P<order_id>\d+)/$', views.send_confiramtion_email, name='restaurant_confirm'),
                       )
