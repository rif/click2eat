from django.conf.urls.defaults import *
from restaurant import views
from django.views.generic import list_detail
from restaurant.models import Unit

#sport_context = {'extra_context': {'sport_list': Sport.objects.annotate(Count('matchday_sport'))}}
#feeds = {'latest': LatestMatchDays, 'news': LatestNews}

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^platinum/$', views.get_random_platinum, name='get_random_platinum'),
                       url(r'^gold/$', views.get_random_gold, name='get_random_gold'),
                       #url(r'^restaurant/(?P<object_id>\d+)/$', list_detail.object_detail, {'queryset': Unit.objects.all()}, name='restaurant_detail'),
                       url(r'^restaurant/(?P<object_id>\d+)/$', views.unit_detail, name='restaurant_detail'),
                       url(r'^feedback/(?P<unit_id>\d+)/$', views.feedback, name='feedback'),
                       )
