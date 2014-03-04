from django import forms

from .models import Entry


class CodeUploadForm(forms.ModelForm):
    class Meta:
        fields = 'code',
        model = Entry
