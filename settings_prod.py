from settings_dev import *
import djcelery

djcelery.setup_loader()


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

INSTALLED_APPS += ('sentry.client','djcelery')

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
ENVELOPE_EMAIL_RECIPIENTS = ('c.precup@filemaker-solutions.ro', 'm.patroescu@filemaker-solutions.ro', 'r.fericean@filemaker-solutions.ro')

SENTRY_REMOTE_URL = 'http://click2eat.ro:9000/store/'
SENTRY_CLIENT = 'sentry.client.async.AsyncSentryClient'
SENTRY_KEY = 'mamaaremere'

BROKER_TRANSPORT = "redis"

BROKER_HOST = "localhost"  # Maps to redis host.
BROKER_PORT = 6379         # Maps to redis port.
BROKER_VHOST = "2"         # Maps to database number.

# CELERY_RESULT_BACKEND = "redis"
# CELERY_REDIS_HOST = "localhost"
# CELERY_REDIS_PORT = 6379
# CELERY_REDIS_DB = 2

CELERY_IGNORE_RESULT = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'class': 'sentry.client.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '()': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}