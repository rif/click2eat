from django.conf.urls.defaults import *
from order import views
from django.views.generic import list_detail
from order.models import Order

urlpatterns = patterns('',
                       url(r'^list/$', views.list, name='list'),
                       url(r'^(?P<object_id>\d+)/$', list_detail.object_detail, {'queryset': Order.objects.all()}, name='detail'),
                       url(r'^create/(?P<unit_id>\d+)/$', views.create, name='create'),
                       url(r'^add_item/(?P<item_id>\d+)/$', views.add_item, name='add_item'),
                       )
