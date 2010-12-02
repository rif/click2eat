from django import forms
from tinymce.widgets import TinyMCE
from menu.models import MenuOfTheDay

class MenuOfTheDayForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs={'theme': 'advanced',}))

    class Meta:
        model = MenuOfTheDay
