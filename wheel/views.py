from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from annoying.decorators import render_to
from datetime import date
from menu.models import Item


@render_to('wheel/random_item.html')
def fortune_ajax(request):
    item = Item.objects.filter(fortune=True).select_related('item_group').order_by('?')[0]
    command_link = ''
    if request.user.is_authenticated():
        command_link = '<a onclick="addItem(\'%(href)s\', \'%(redir)s\'); return false;" href="#">%(order_now)s</a>' % \
            {'redir': reverse("restaurant:detail", args=[item.item_group.unit_id]),
             'href': reverse("order:add_item", args=[item.id, request.user.username]),
             'order_now': _('Order this Item')}
    if not item: item = _('No item yet defined!')
    return locals()
