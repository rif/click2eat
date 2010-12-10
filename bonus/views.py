from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from bonus.models import Bonus

@login_required
@render_to('bonus/history.html')
def history(request):
    bonuses = Bonus.objects.filter(user__id = request.user.id)
    return {'object_list': bonuses}
