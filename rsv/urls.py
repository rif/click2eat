from django.conf.urls.defaults import patterns, url
from rsv.views import IndexView
from mobile import views


urlpatterns = patterns('',
    url(r'^', IndexView.as_view(), name='index'),
)