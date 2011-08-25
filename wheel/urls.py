from django.conf.urls.defaults import *
from wheel import views


urlpatterns = patterns('django.views.generic.simple',
                       url(r'^sample/$', views.fortune_ajax, name='fortune_ajax'),
                       )
