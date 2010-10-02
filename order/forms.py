from django import forms
from order.models import Order

class CartNameForm(forms.Form):
    name = forms.CharField(max_length=10)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'additional_info')