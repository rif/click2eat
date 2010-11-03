from django import forms
from tinymce.widgets import TinyMCE
from restaurant.models import Unit

class UnitForm(forms.ModelForm):
    info = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs={'theme': 'advanced',}))

    class Meta:
        model = Unit
