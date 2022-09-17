from django import forms

from .models import Declaration, DeclarationResponse


class ActivationForm(forms.Form):
    activation_code = forms.CharField(max_length=256)


class DeclarationForm(forms.ModelForm):
    class Meta:
        model = Declaration
        fields = [
            'title',
            'text',
            'category',
            'upload',
        ]


class DeclarationResponseForm(forms.ModelForm):
    class Meta:
        model = DeclarationResponse
        fields = [
            'text'
        ]
