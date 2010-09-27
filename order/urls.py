from django.conf.urls.defaults import *
from order import views
from django.views.generic import list_detail
from order.models import Order

urlpatterns = patterns('',
                       url(r'^list/$', views.list, name='list'),
                       url(r'^(?P<object_id>\d+)/$', list_detail.object_detail, {'queryset': Order.objects.all(), 'template_object_name': 'order'}, name='detail'),
                       #url(r'^create/(?P<unit_id>\d+)/$', views.create, name='create'),
                       url(r'^add_item/(?P<item_id>\d+)/(?P<cart_name>.+)/$', views.add_item, name='add_item'),
                       url(r'^remove_item/(?P<item_id>\d+)/$', views.remove_item, name='remove_item'),
                       url(r'^get_current/(?P<unit_id>\d+)/$', views.get_current_order, name='get_current'),
                       url(r'^send/(?P<unit_id>\d+)/$', views.send, name='send'),
                       url(r'^get_total_amount/(?P<unit_id>\d+)/$', views.get_total_amount, name='get_total_amount'),
                       url(r'^add_cart/(?P<unit_id>\d+)/$', views.add_cart, name='add_cart'),
                       )
