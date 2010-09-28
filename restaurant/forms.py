from django import forms
from restaurant.models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ('user', 'restaurant')