from django import forms
from django.utils.translation import ugettext_lazy as _
#from django.db.models import F
from order.models import Order
from userprofiles.models import DeliveryAddress

class CartNameForm(forms.Form):
    name = forms.CharField(max_length=10)

class OrderForm(forms.ModelForm):
    #address = forms.ModelChoiceField(queryset=DeliveryAddress.objects.filter(user = F('user')))
    
    def clean_address(self):
        address = self.cleaned_data['address']
        if not address:
            raise forms.ValidationError(_('Please select a delivery address'))
        return address

    class Meta:
        model = Order
        fields = ('address', 'additional_info',)