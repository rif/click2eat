from django.conf.urls.defaults import *
from userprofiles import views
from userprofiles.models import DeliveryAddress
from django.core.urlresolvers import reverse

urlpatterns = patterns('django.views.generic.create_update',
                       url(r'^create/$', views.create, name='create_address'),
                       url(r'^update/(?P<object_id>\d+)/$', 'update_object', {'model': DeliveryAddress, 'login_required': True}, name='update_address'),
                       url(r'^delete/(?P<object_id>\d+)/$', 'delete_object', {'model': DeliveryAddress, 'post_delete_redirect': reverse('restaurant:index'), 'login_required': True}, name='delete_address'),
                       )

urlpatterns += patterns('django.views.generic.list_detail',
                       url(r'^addrdetail/(?P<object_id>\d+)/$$', 'object_detail', {'queryset': DeliveryAddress.objects.all()}, name='address_detail'),
                       )
