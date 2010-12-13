from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from datetime import date
from menu.models import MenuOfTheDay

def fortune_ajax(request):
    if not request.user.is_authenticated():
        return HttpResponse(_('Please login!'))
    motd = MenuOfTheDay.objects.filter(day = date.today()).order_by('?')
    if motd.exists():
	motd = motd[0].name
    else:
	motd = _('No menu of the day defined!')
    return HttpResponse(motd)


