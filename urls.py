from django.conf.urls.defaults import *
from django.contrib import admin
from userprofiles import views
from userprofiles.forms import BucatarRegistrationForm
from restaurant.sitemaps import UnitSitemap

sitemaps = {'units': UnitSitemap}

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^', include('restaurant.urls', namespace='restaurant')),
                       (r'^menu/', include('menu.urls', namespace='menu')),
                       (r'^order/', include('order.urls', namespace='order')),
                       (r'^userprofiles/', include('userprofiles.urls', namespace='userprofiles')),
                       (r'^wheel/', include('wheel.urls', namespace='wheel')),
                       (r'^bonus/', include('bonus.urls', namespace='bonus')),
                       (r'^mobile/', include('mobile.urls', namespace='mobile')),
                       (r'^admin/filebrowser/', include('filebrowser.urls')),
                       (r'^grappelli/', include('grappelli.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/register/$', 'registration.views.register',
                           {'form_class': BucatarRegistrationForm, 'backend': 'userprofiles.forms.BucatarRegistrationBackend'},
                           name='registration_register'),
                       (r'^accounts/', include('registration.backends.default.urls')),
                       (r'^i18n/', include('django.conf.urls.i18n')),
                       (r'^sentry/', include('sentry.web.urls')),
                       (r'^tinymce/', include('tinymce.urls')),
                       (r'^avatar/', include('avatar.urls')),
                       (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
                       (r'^flat/', include('django.contrib.flatpages.urls')),
                       (r'^robots.txt$', include('robots.urls')),
                       (r'^contact/',    include('envelope.urls')),
                       url(r'^rosetta/', include('rosetta.urls'))
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
                        url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/images/favicon.ico'}),
                        )
