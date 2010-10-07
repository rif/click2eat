from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('restaurant.urls', namespace='restaurant')),
    (r'^menu/', include('menu.urls', namespace='menu')),
    (r'^order/', include('order.urls', namespace='order')),
    (r'^userprofiles/', include('userprofiles.urls', namespace='userprofiles')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^sentry/', include('sentry.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns += patterns('profiles.views',
                       url(r'^profiles/create/$', 'create_profile', name='profiles_create_profile'),
                       url(r'^profiles/edit/$', 'edit_profile', name='profiles_edit_profile'),
                       url(r'^profiles/(?P<username>\w+)/$', 'profile_detail', {'public_profile_field': 'public'}, name='profiles_profile_detail'),
                       url(r'^profiles/$', 'profile_list', {'public_profile_field': 'public'}, name='profiles_profile_list'),
                       )
