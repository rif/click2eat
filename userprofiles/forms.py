from django import forms
from userprofiles.models import DeliveryAddress

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        exclude = ('user', 'geolocated_address', 'latidude', 'longitude', 'geolocation_error')
