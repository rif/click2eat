import os
import sys
import site

site.addsitedir('/Users/rif/.virtualenvs/bucatar/lib/python2.6/site-packages')
sys.path.append('/Users/rif/bucatar')

os.environ['DJANGO_SETTINGS_MODULE'] = 'bucatar.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

