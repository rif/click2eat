from sentry.conf.defaults import *
from sentry.conf.server import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/rif/sentry.db',
     }
}

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 9000

SENTRY_KEY = 'mamaaremere'
SENTRY_PUBLIC = False
