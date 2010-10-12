from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default import DefaultBackend
from annoying.functions import get_object_or_None
from userprofiles.models import DeliveryAddress
from friends.models import JoinInvitation

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        exclude = ('user', 'geolocated_address', 'latitude', 'longitude', 'geolocation_error')
        
class InviteFriendForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(_('message'), initial=_('Join me for lunch!'), widget=forms.Textarea)


class BucatarRegistrationForm(RegistrationFormUniqueEmail):
    captcha = CaptchaField()

class BucatarRegistrationBackend(DefaultBackend):
     def get_form_class(self, request):
         return BucatarRegistrationForm

     def register(self, request, **kwargs):
         new_user = super(BucatarRegistrationBackend, self).register(request, **kwargs)
         if 'confirmation_key' in request.session.keys():
             confirmation_key = request.session['confirmation_key']
             ji = get_object_or_None(JoinInvitation, confirmation_key=confirmation_key)
             if ji != None:
                 ji.accept(new_user)
         return new_user
             
     def activate(self, request, activation_key):
         activate = super(BucatarRegistrationBackend, self).activate(request, activation_key)
         return activated
