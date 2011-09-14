from settings_dev import *

DEBUG = TEMPLATE_DEBUG = False
DATABASES = {
    'default': {
    'ENGINE':	'django.db.backends.mysql',
	'HOST':		'localhost',
    'NAME': 	'click2eat',
	'USER':		'django_login',
	'PASSWORD':	'testus_cumulus'
    }
}
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

INSTALLED_APPS += [
  'sentry.client',
]

SENTRY_REMOTE_URL = 'http://localhost:9000/sentry/store/'
SENTRY_KEY = 'mamaaremere'

ENVELOPE_EMAIL_RECIPIENTS = ('c.precup@filemaker-solutions.ro', 'm.patroescu@filemaker-solutions.ro', 'r.fericean@filemaker-solutions.ro')
