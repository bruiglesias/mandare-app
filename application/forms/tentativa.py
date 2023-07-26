from django import forms
from application.models import Tentativa


class TentativaForm(forms.ModelForm):
    class Meta:
        model = Tentativa
        fields = ['sessao', 'situacao']
