from django import forms
from tinymce.widgets import TinyMCE
from restaurant.models import Unit
from django.contrib.flatpages.models import FlatPage

class FlatPageForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs={'theme': 'advanced',}))

    class Meta:
        model = FlatPage

class UnitForm(forms.ModelForm):
    info = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs={'theme': 'advanced',}))

    class Meta:
        model = Unit
