from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from order.models import Order
from userprofiles.models import DeliveryAddress

class CartNameForm(forms.Form):
    name = forms.CharField(max_length=10)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'additional_info')