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
SENTRY_LOG_DIR= '/home/rif/'
SENTRY_RUN_DIR= '/home/rif/'

SENTRY_KEY = '2d56cabc3073637ff33471e2ec84de27f99180f6'
SENTRY_PUBLIC = False
SENTRY_WEB_OPTIONS = {
    'workers': 1,  # the number of gunicorn workers
    'worker_class': 'gevent',
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'testus_cumulus'
EMAIL_HOST_USER = 'click2eat@click2eat.ro'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[Sentry Click2eat.ro] '
