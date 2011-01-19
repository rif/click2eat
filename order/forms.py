from django import forms
from order.models import Order, Rating
from restaurant.models import DeliveryType
from django.utils.translation import ugettext_lazy as _

class CartNameForm(forms.Form):
    name = forms.CharField(max_length=10)

class OrderForm(forms.ModelForm):
    delivery_type = forms.ModelChoiceField(queryset=DeliveryType.objects.all())
    def clean_address(self):
        address = self.cleaned_data['address']
        delivery_type = self.cleaned_data['delivery_type']

        if delivery_type.require_address and address == None:
            raise forms.ValidationError(_("Please specify a delivery address"))

        return address

    class Meta:
        model = Order
        # delivery_type and address will be (re)defined in the view
        fields = ('delivery_type', 'address', 'additional_info')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ('user', 'order')
