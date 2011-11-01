from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from django.db.models import Sum
from datetime import datetime
from bonus.models import BonusTransaction

@login_required
@render_to('bonus/history.html')
def history(request):
    bonuses = BonusTransaction.objects.filter(user__id = request.user.id)
    return {'object_list': bonuses}
