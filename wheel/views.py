from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to

@login_required
@render_to('wheel/fortune.html')
def fortune(request):
    return {'result': 'mancare'}


