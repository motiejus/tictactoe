from django import forms

from .models import Entry


class CodeUploadForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea)
