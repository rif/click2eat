from django.conf.urls.defaults import patterns, url
from rsv import views

urlpatterns = patterns('',
    url(r'^', views.index, name='index'),
)