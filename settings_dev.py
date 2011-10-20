import os
from django.utils.translation import ugettext_lazy as _
import djcelery

djcelery.setup_loader()

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Radu Ioan Fericean', 'fericean@gmail.com'),
)

MANAGERS = ADMINS

SERVER_EMAIL = "click2eat.ro@gmail.com"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bucatar.sqlite',
    }
}

TIME_ZONE = 'Europe/Bucharest'
LANGUAGE_CODE = 'ro'
ugettext = lambda s: s

LANGUAGES = (
  ('ro', ugettext('Romanian')),
  ('en', ugettext('English')),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'click2eat.ro@gmail.com'
EMAIL_HOST_PASSWORD = 'testus_cumulus'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = ' [Click2eat.ro] '

SITE_NAME = 'bucatar'
CONTACT_EMAIL = 'contact@mailinator.com'
DEFAULT_FROM_EMAIL = 'default@mailinator.com'

ACCOUNT_ACTIVATION_DAYS = 7
PAGINATION_DEFAULT_WINDOW = 3

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 1,
            #'PASSWORD': 'yadayada',
            #'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

CAPTCHA_NOISE_FUNCTIONS =  ('captcha.helpers.noise_dots',) # ('captcha.helpers.noise_arcs','captcha.helpers.noise_dots',)

STATIC_ROOT = rel('static')
STATIC_URL = '/static/'
MEDIA_ROOT = rel('static/upload')
MEDIA_URL =  '/static/upload/'

#ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'
FILEBROWSER_DIRECTORY=''

STATICFILES_DIRS = (
    rel('media'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '-4+i0ac6q-$7e@!sy55hlbmb*4)2+a5oc!ah2@5rn9gqlurk-#'

LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = '/'
AUTH_PROFILE_MODULE = 'userprofiles.UserProfile'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    )

AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = 'bucatar.urls'

TEMPLATE_DIRS = (
    rel('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    # external apps
    'profiles',
    'registration',
    'django_extensions',
    'south',
    'uni_form',
    'friends',
    'captcha',
    'taggit',
    'pagination',
    'django_filters',
    'tinymce',
    'avatar',
    'robots',
    'honeypot',
    'envelope',
    'newsletter',
    'djcelery',
    'biblion',
    'sorl.thumbnail',
    # my apps
    'restaurant',
    'menu',
    'userprofiles',
    'order',
    'wheel',
    'bonus',
    'mobile',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',
                       'rosetta-grappelli',
                       'rosetta',
                       'django.contrib.sessions', # session in database
                       )

INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
}

ENVELOPE_EMAIL_RECIPIENTS=('r.fericean@filemaker-solutions.ro',)

ENVELOPE_CONTACT_CHOICES = (
    ('',    _("Choose")),
    (10,    _("A general question regarding the website")),
    (20,    _("Suggestion")),
    (30,    _("Unsatisfactory service")),
    (40,    _("Site functionality problem")),
    (None,  _("Other")),
)

BIBLION_ALL_SECTION_NAME = _('all')
BIBLION_SECTIONS = (('news',_('news')), ('promo', _('promotions')))

HONEYPOT_FIELD_NAME = 'information'

TINYMCE_JS_URL = STATIC_URL + 'js/tiny_mce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}

GRAPPELLI_INDEX_DASHBOARD = 'bucatar.dashboard.CustomIndexDashboard'
GRAPPELLI_ADMIN_TITLE = 'Click2eat'

BROKER_TRANSPORT = 'redis'
BROKER_HOST = 'localhost'  # Maps to redis host.
BROKER_PORT = 6379         # Maps to redis port.
BROKER_VHOST = '2'         # Maps to database number.

#CELERY_RESULT_BACKEND = "redis"
#CELERY_REDIS_HOST = "localhost"
#CELERY_REDIS_PORT = 6379
#CELERY_REDIS_DB = 2

CELERY_IGNORE_RESULT = True

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_HOST = 'localhost'
THUMBNAIL_REDIS_PORT = 6379
THUMBNAIL_REDIS_DB = 3
THUMBNAIL_REDIS_PASSWORD = ''
THUMBNAIL_DEBUG = True