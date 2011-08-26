from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from annoying.decorators import render_to
from datetime import date
from menu.models import MenuOfTheDay


@render_to('wheel/random_daily_menu.html')
def fortune_ajax(request):
    motd = MenuOfTheDay.objects.filter(day = date.today()).order_by('?')
    if motd.exists():
        motd = motd[0]
        command_link = '<a onclick="addMotd(\'%(href)s\', \'%(redir)s\'); return false;" href="#">%(order_now)s</a>' % \
            {'redir': reverse("restaurant:detail", args=[motd.unit.id]),
             'href': reverse("order:add_motd", args=[motd.id, request.user.username]),
             'order_now': _('Order this menu')}
    else:
        motd = _('No menu of the day defined!')
    return locals()
