from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from annoying.decorators import render_to
from time import time
from menu.models import Item


@render_to('wheel/random_item.html')
def fortune_ajax(request):
    item = Item.objects.filter(fortune=True).select_related('item_group').order_by('?')[0]
    command_link = ''
    if request.user.is_authenticated():
        command_link = '<a onclick="addItem(\'%(href)s\', \'%(redir)s\'); return false;" href="#">%(order_now)s</a>' % \
            {'redir': reverse("restaurant:detail", args=[item.item_group.unit_id]),
             'href': reverse("order:shop", args=[item.item_group.unit_id, request.user.username, '%s!%s-0' % (int(time()*1000), item.id)]), # with time() we generate the analogous javascript uid
             'order_now': _('Order this Item')}
    if not item: item = _('No item yet defined!')
    return locals()
