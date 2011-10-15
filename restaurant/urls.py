from django.conf.urls.defaults import *
from restaurant import views
from django.views.generic import list_detail
from restaurant.models import Unit

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^unitlist/$', views.unit_list, name='list'),
                       url(r'^unit/(?P<unit_id>\d+)/$', views.unit_detail, name='detail'),
                       url(r'^comments/(?P<unit_id>\d+)/$', views.unit_comments, name='comments'),
                       #url(r'^history/(?P<unit_id>\d+)/$', views.package_history, name='package_history'),
                       url(r'^invoice/(?P<unit_id>\d+)/$', views.invoice, name='invoice'),
                       url(r'^package_history/(?P<unit_id>\d+)/$', views.package_history, name='package_history'),                      
                       )

urlpatterns += patterns('django.views.generic.simple',
                       url(r'^admini/$', 'direct_to_template', {'template': 'restaurant/administrator.html'}, name='administrator'),
)
