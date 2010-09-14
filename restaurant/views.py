from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello bucatar")
