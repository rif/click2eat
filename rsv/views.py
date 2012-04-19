from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.contrib.auth.models import User
from redis_sessions import session
from rsv.forms import QueryForm
import redis
import base64
import cPickle as pickle

@login_required
@render_to('rsv/index.html')
def index(request):
    if not request.user.is_staff: raise PermissionDenied()

    r = redis.StrictRedis(host=getattr(settings, 'SESSION_REDIS_HOST', 'localhost'),
        port=getattr(settings, 'SESSION_REDIS_PORT', 6379),
        db=getattr(settings, 'SESSION_REDIS_DB', 0),
        password=getattr(settings, 'SESSION_REDIS_PASSWORD', None)
        )
    ss = session.SessionStore()
    sessions = []
    query = '*'            
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] + '*'
    else:
        form = QueryForm() # An unbound form    
        
    for session_id in r.keys(query):
        d = ss.decode(r.get(session_id))
        if '_auth_user_id' in d:
            user = cache.get('_auth_user_id%s' % d['_auth_user_id'])
            if not user:
                user = User.objects.get(pk=d['_auth_user_id'])
                cache.set('_auth_user_id%s' % d['_auth_user_id'], user, 30)
            a = {'key': session_id, 'user': user}
            sessions.append(a)
    order_count = Order.objects.count()
    return {'form': form, 'sessions': sessions, 'order_count': order_count}
    
