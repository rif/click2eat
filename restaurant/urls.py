from django.conf.urls.defaults import *
from restaurant import views
#from restaurant import models

#sport_context = {'extra_context': {'sport_list': Sport.objects.annotate(Count('matchday_sport'))}}
#feeds = {'latest': LatestMatchDays, 'news': LatestNews}

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^platinum/$', views.get_random_platinum, name='get_random_platinum'),
                       url(r'^gold/$', views.get_random_gold, name='get_random_gold'),
                       )
