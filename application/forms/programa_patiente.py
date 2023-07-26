from django import forms
from application.models import ProgramaPaciente


class ProgramaPacienteForm(forms.ModelForm):
    class Meta:
        model = ProgramaPaciente
        fields = ['programa', 'paciente']
