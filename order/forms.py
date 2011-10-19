from django import forms
from order.models import Order, Rating
from restaurant.models import DeliveryType
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

class CartNameForm(forms.Form):
    name = forms.CharField(max_length=10)

class OrderForm(forms.ModelForm):    
    delivery_type = forms.ModelChoiceField(queryset=DeliveryType.objects.all())
    def clean_address(self):
        address = self.cleaned_data['address']
        delivery_type = None
        if self.cleaned_data.has_key('delivery_type'):
            delivery_type = self.cleaned_data['delivery_type']

        if (delivery_type and delivery_type.require_address) and address == None:
            raise forms.ValidationError(_("Please specify a delivery address"))

        return address

    def clean_desired_delivery_time(self):
        desired_delivery_time = None
        if self.cleaned_data.has_key('desired_delivery_time'):
            desired_delivery_time = self.cleaned_data['desired_delivery_time']

        if desired_delivery_time and desired_delivery_time < datetime.now():
            raise forms.ValidationError(_('Please set a future desired time'))
        
        unit = self.unit # injected from view
        if not unit.is_open() and (not desired_delivery_time or not unit.is_open_at(desired_delivery_time)):
            raise forms.ValidationError(_('As the restaurant is closed please set a desired delivery time in the restaurant open hours range.'))
    

    class Meta:
        model = Order
        # delivery_type and address will be (re)defined in the view
        fields = ('delivery_type', 'address', 'desired_delivery_time', 'additional_info')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ('user', 'order')
