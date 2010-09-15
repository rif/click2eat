from settings_dev import *

DEBUG = TEMPLATE_DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': '/bucatar_data/bucatar.db',
    }
}
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ustest@gmail.com'
EMAIL_HOST_PASSWORD = 'greta.1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = ' [bucatar] '

LOGIN_URL="/stand/accounts/login/"

SERVER='apache.filemaker-solutions.ro'
MEDIA_URL = 'http://%s/static/media/' % SERVER
ADMIN_MEDIA_PREFIX = 'http://%s/static/admin/media/' % SERVER

