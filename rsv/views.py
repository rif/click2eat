from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from redis_sessions import session 
import redis
import base64
import cPickle as pickle

class IndexView(TemplateView):
    template_name = "rsv/index.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_staff: raise PermissionDenied()
        context = super(IndexView, self).get_context_data(**kwargs)                

        r = redis.StrictRedis(host=getattr(settings, 'SESSION_REDIS_HOST', 'localhost'),
            port=getattr(settings, 'SESSION_REDIS_PORT', 6379),
            db=getattr(settings, 'SESSION_REDIS_DB', 0),
            password=getattr(settings, 'SESSION_REDIS_PASSWORD', None)
            )
        ss = session.SessionStore()
        sessions = []
        for session_id in r.keys('*'):
            d = ss.decode(r.get(session_id))
            if '_auth_user_id' in d:
                a = {'key': session_id, 'user': User.objects.get(pk=d['_auth_user_id'])}
                sessions.append(a)

        context['sessions'] = sessions
        return context