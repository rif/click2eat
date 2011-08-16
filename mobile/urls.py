from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from mobile import views


urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name="mobile/home.html")),
                       )