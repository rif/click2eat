from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse

def index(request):
    if request.user.is_authenticated():
        return HttpResponse('Hello %s, you can logout <a href="%s">here</a>' % (request.user, "/accounts/logout/"))
    else:
        return HttpResponse('Hello %s, please <a href="%s">login</a>' % (request.user, "/accounts/login/"))
