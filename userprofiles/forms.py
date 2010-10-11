from django import forms
from django.utils.translation import ugettext_lazy as _
from userprofiles.models import DeliveryAddress

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        exclude = ('user', 'geolocated_address', 'latitude', 'longitude', 'geolocation_error')
        
class InviteFriendForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(_('message'), initial=_('Join me for lunch!'), widget=forms.Textarea)
