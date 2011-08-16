from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from mobile import views


urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name='mobile/home.html'), name='home'),
                       url(r'^units/$', views.units, name='units'),
                       url(r'^menu/(?P<unit_id>\d+)/$', views.menu, name='menu'),
                       url(r'^accounts/login/$','django.contrib.auth.views.login', {'template_name':'mobile/login.html'},name='login'),
                       url(r'^accounts/logout/$','django.contrib.auth.views.logout',{'template_name':'mobile/logout.html'}, name='logout'),
                       )
