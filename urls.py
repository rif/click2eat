from django.conf.urls.defaults import *
from django.contrib import admin
from userprofiles import views
from userprofiles.forms import BucatarRegistrationForm

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^', include('restaurant.urls', namespace='restaurant')),
                       (r'^menu/', include('menu.urls', namespace='menu')),
                       (r'^order/', include('order.urls', namespace='order')),
                       (r'^userprofiles/', include('userprofiles.urls', namespace='userprofiles')),
                       (r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/register/$', 'registration.views.register',
                           {'form_class': BucatarRegistrationForm, 'backend': 'userprofiles.forms.BucatarRegistrationBackend'},
                           name='registration_register'),
                       (r'^accounts/', include('registration.backends.default.urls')),
                       (r'^i18n/', include('django.conf.urls.i18n')),
                       (r'^sentry/', include('sentry.urls')),
                       )

urlpatterns += patterns('profiles.views',
                        url(r'^profiles/create/$', 'create_profile', name='profiles_create_profile'),
                        url(r'^profiles/edit/$', 'edit_profile', name='profiles_edit_profile'),
                        url(r'^profiles/(?P<username>\w+)/$', views.profile_detail, name='profiles_profile_detail'),
                        url(r'^profiles/$', 'profile_list', {'public_profile_field': 'public'}, name='profiles_profile_list'),
                        )

urlpatterns += patterns('',
                        url(r'^inviteaccept/(?P<confirmation_key>\w+)/$', views.invite_accept, name='friends_accept_join'),
			url(r'^captcha/', include('captcha.urls')),
                        )
