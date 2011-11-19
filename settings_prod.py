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

INSTALLED_APPS += ('raven.contrib.django',)

ENVELOPE_EMAIL_RECIPIENTS = ('office@click2eat.ro')

SENTRY_SERVERS = ['http://click2eat.ro:9000/store/']
SENTRY_KEY = 'mamaaremere'

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
