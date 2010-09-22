from django import forms
from userprofiles.models import DeliveryAddress

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        exclude = ('user')