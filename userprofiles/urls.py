from django.conf.urls.defaults import *
from userprofiles import views
from userprofiles.forms import DeliveryAddressForm
from userprofiles.models import DeliveryAddress

urlpatterns = patterns('',
                       url(r'^createaddress/$', views.create, name='create_address'),
                       url(r'^updateaddress/(?P<object_id>\d+)/$', views.limited_update_object, {'form_class': DeliveryAddressForm, 'login_required': True}, name='update_address'),
                       url(r'^deleteaddress/(?P<object_id>\d+)/$', views.limited_delete_object, {'model': DeliveryAddress, 'login_required': True}, name='delete_address'),
                       url(r'^addrdetail/(?P<object_id>\d+)/$', views.limited_object_detail, {'queryset': DeliveryAddress.objects.all()}, name='address_detail'),
                       url(r'^geoerror/(?P<object_id>\d+)/$', views.mark_geolocation_error, name='geolocation_error'),
                       )

urlpatterns += patterns('',
                         url(r'^invitefriend/$', views.invite_friend, name='invite_friend'),
                        )
