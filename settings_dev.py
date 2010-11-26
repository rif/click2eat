import os

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Radu Ioan Fericean', 'r.fericean@filemaker-solutions.ro'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bucatar.sqlite',
    }
}

TIME_ZONE = 'Europe/Bucharest'
LANGUAGE_CODE = 'ro-ro'
ugettext = lambda s: s

LANGUAGES = (
  ('ro', ugettext('Romanian')),
  ('en', ugettext('English')),
  ('de', ugettext('German')),
  ('fr', ugettext('French')),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True

# email settings
#EMAIL_HOST = 'mail.filemkaer-solutions.ro'
#EMAIL_PORT = '25'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ustest@gmail.com'
EMAIL_HOST_PASSWORD = 'greta.1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = ' [bucatar] '

SITE_NAME = 'bucatar'
CONTACT_EMAIL = 'contact@mailinator.com'
DEFAULT_FROM_EMAIL = 'default@mailinator.com'

ACCOUNT_ACTIVATION_DAYS = 7
PAGINATION_DEFAULT_WINDOW = 3

CACHE_BACKEND = 'locmem://'

CAPTCHA_NOISE_FUNCTIONS =  ('captcha.helpers.noise_dots',) # ('captcha.helpers.noise_arcs','captcha.helpers.noise_dots',)

DJANGO_MEMCACHED_REQUIRE_STAFF = True

MEDIA_ROOT = rel('media')
MEDIA_URL =  '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

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
    'annoying.middlewares.StaticServe',
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
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
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
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # external apps
    'profiles',
    'registration',
    'django_extensions',
    'south',
    'uni_form',
    'indexer',
    'paging',
    'sentry',
    'sentry.client',
    'friends',
    'captcha',
    'taggit',
    'pagination',
    'memcache_status',
    'django_filters',
    'tinymce',
    'compressor',
    'avatar',
    'rosetta',
    # my apps
    'restaurant',
    'menu',
    'userprofiles',
    'order',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': True,
}
