from django import forms
from .models import Art, Tag


class ArtForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Art
        fields = '__all__'
