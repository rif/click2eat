from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from datetime import date
from menu.models import MenuOfTheDay

def fortune_ajax(request):
    if not request.user.is_authenticated():
        return HttpResponse(_('Please login!'))
    motd = MenuOfTheDay.objects.filter(day = date.today()).order_by('?')
    if motd.exists():
	motd = motd[0]
        motd = '<a onclick="addMotd(\'%(href)s\', \'%(redir)s\'); return false;" href="#">%(motd_name)s</a>' % \
            {'redir': reverse("restaurant:detail", args=[motd.id]),
             'href': reverse("order:add_motd", args=[motd.id, request.user.username]),
             'motd_name': motd.name}
    else:
	motd = _('No menu of the day defined!')
    return HttpResponse(motd)


