from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('restaurant.urls', namespace='restaurant')),
    (r'^admin/', include(admin.site.urls)),
    (r'^profiles/', include('profiles.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

# if we're in DEBUG mode, allow django to serve media
# This is considered inefficient and isn't secure.
from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
