from django import forms

class CartNameForm(forms.Form):
    name = forms.CharField(max_length=10)
