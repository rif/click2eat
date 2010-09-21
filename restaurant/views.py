from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

def index(request):
    try:
        if request.user.get_profile() != None:
            return render_to_response('restaurant/index.html', context_instance=RequestContext(request))
        else:
            return redirect('profiles_create_profile')
    except:
        return redirect('profiles_create_profile')

