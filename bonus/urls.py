from django.conf.urls.defaults import *
from bonus import views


urlpatterns = patterns('',
                       url(r'^history/$', views.history, name='history'),
                       )
