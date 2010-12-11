from django.conf.urls.defaults import *
from wheel import views


urlpatterns = patterns('django.views.generic.simple',
                       url(r'^$', 'direct_to_template', {'template': 'wheel/fortune.html'}, name='fortune'),
                       url(r'^sample/$', views.fortune_ajax, name='fortune_ajax'),
                       )
