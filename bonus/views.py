from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to, ajax_request
from django.db.models import Sum
from datetime import datetime
from bonus.models import Bonus

@login_required
@render_to('bonus/history.html')
def history(request):
    bonuses = Bonus.objects.filter(user__id = request.user.id).order_by('-received_date')
    return {'object_list': bonuses}
