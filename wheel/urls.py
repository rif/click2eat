from django.conf.urls.defaults import *
from wheel import views


urlpatterns = patterns('',
                       url(r'^$', views.fortune, name='fortune'),
                       )
