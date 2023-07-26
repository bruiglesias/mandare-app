from django import forms
from application.models import Paciente
import re


class PacienteForm(forms.ModelForm):

    foto_perfil = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'accept': "image/jpeg, image/png, image/jpg",
            'oninput': "changePhoto()"
        })
    )

    nome = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o nome do paciente',
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'autocomplete': "off",
        }))

    data_nascimento = forms.CharField(
        required=False,
        max_length=10,
        error_messages={
            'invalid_date': "A data possui o formato correto mas é uma data inválida."  # noqa
        },
        widget=forms.TextInput(attrs={
            'placeholder': "dd/mm/aaaa",
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'oninput': "formatarData('id_data_nascimento')",
            'autocomplete': "off"
        }))

    especialidade = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Selecione a especialidade"),
            ("Psicologia", "Psicologia"),
        ],
        widget=forms.Select(
            attrs={
                'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5"  # noqa
            }
        )
    )

    diagnostico = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Autismo',
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'autocomplete': "off",
        }))

    class Meta:
        model = Paciente
        fields = [
            'nome',
            'foto_perfil',
            'data_nascimento',
            'especialidade',
            'profissional',
            'diagnostico'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = ''

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) == 0:
            raise forms.ValidationError(
                'O campo nome é obrigarório.',
                code='required'
            )

        if len(nome.split()) < 2:
            raise forms.ValidationError(
                'Insira seu nome completo',
                code='invalid'
            )

        padrao = r'^[a-zA-ZÀ-ÿ\s]+$'
        if not re.match(padrao, nome):
            raise forms.ValidationError(
                'O nome possui caracteres inválidos.',
                code='invalid'
            )

        return nome

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if len(data_nascimento) == 0:
            raise forms.ValidationError(
                'O campo data de nascimento é obrigarório.',
                code='required'
            )

        return data_nascimento

    def clean_especialidade(self):
        especialidade = self.cleaned_data.get('especialidade')
        if especialidade is None or len(especialidade) == 0:
            raise forms.ValidationError(
                'O campo especialidade é obrigarório.',
                code='required'
            )

        return especialidade

    def clean_diagnostico(self):
        diagnostico = self.cleaned_data.get('diagnostico')
        if len(diagnostico) == 0:
            raise forms.ValidationError(
                'O campo diagnostico é obrigarório.',
                code='required'
            )

        return diagnostico

    def save(self, commit=True):
        paciente = super().save(commit=False)
        paciente.profissional = self.cleaned_data["profissional"]
        if commit:
            paciente.save()
        return paciente
