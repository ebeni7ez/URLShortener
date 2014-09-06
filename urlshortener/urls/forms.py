"""
    Include the form for submiting an URL
    that will be shortened
"""

from django import forms

class LinkForm(forms.Form):
    url = forms.URLField(label='Insert your URL:')
