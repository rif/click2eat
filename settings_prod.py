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
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ustest@gmail.com'
EMAIL_HOST_PASSWORD = 'greta.1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = ' [click2eat] '

ENVELOPE_EMAIL_RECIPIENTS = ('c.precup@filemaker-solutions.ro', 'm.patroescu@filemaker-solutions.ro', 'r.fericean@filemaker-solutions.ro')
