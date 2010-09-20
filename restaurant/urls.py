from django.conf.urls.defaults import *
from restaurant import views
from restaurant.models import *
from userprofiles.forms import UserRegistrationForm, UserProfileForm

#sport_context = {'extra_context': {'sport_list': Sport.objects.annotate(Count('matchday_sport'))}}
#feeds = {'latest': LatestMatchDays, 'news': LatestNews}

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       )
