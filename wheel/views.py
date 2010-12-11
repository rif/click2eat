from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import date
from menu.models import MenuOfTheDay

@login_required
def fortune_ajax(request):
    motd = MenuOfTheDay.objects.filter(day = date.today()).order_by('?')
    if motd.exists():
	motd = motd[0].name
    else:
	motd = 'Not Found'
    return HttpResponse(motd)


