from django import forms
from taggit.models import Tag

class TagSelectForm(forms.Form):
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        empty_label=None,
        label="Select Tag",
        initial=lambda: Tag.objects.filter(name__iexact="General Culture").first()
    )
