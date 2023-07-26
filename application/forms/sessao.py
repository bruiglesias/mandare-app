from django import forms
from application.models import Sessao


class SessaoForm(forms.ModelForm):
    class Meta:
        model = Sessao
        fields = ['nome', 'programa']
