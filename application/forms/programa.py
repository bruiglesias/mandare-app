from django import forms
from application.models import Programa


class ProgramaForm(forms.ModelForm):

    nome = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o nome do programa',
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'autocomplete': "off",
        }))

    numero_sessoes = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg block w-full p-2.5',
            'oninput': "formatarNumero('id_numero_sessoes')",
        })
    )

    numero_tentativas = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg block w-full p-2.5',
            'oninput': "formatarNumero('id_numero_tentativas')",
        })
    )

    class Meta:
        model = Programa
        fields = ['profissional', 'nome',
                  'numero_sessoes', 'numero_tentativas']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''

    def clean(self):
        cleaned_data = super().clean()
        profissional = cleaned_data.get('profissional')
        nome = cleaned_data.get('nome')
        numero_sessoes = cleaned_data.get('numero_sessoes')
        numero_tentativas = cleaned_data.get('numero_tentativas')

        # Verificar se já existe um programa com os mesmos campos
        programa_existente = Programa.objects.filter(
            profissional=profissional,
            nome=nome,
            numero_sessoes=numero_sessoes,
            numero_tentativas=numero_tentativas
        ).exists()

        if programa_existente:
            self.add_error('nome', forms.ValidationError(
                "Um programa com esse nome, numero de sessões e tentativas já existe."))  # noqa

        return cleaned_data

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) == 0:
            raise forms.ValidationError(
                'O campo nome é obrigarório.',
                code='required'
            )

        return nome

    def clean_numero_sessoes(self):
        numero_sessoes = self.cleaned_data.get('numero_sessoes')
        if numero_sessoes is None or numero_sessoes < 1:
            raise forms.ValidationError(
                'O campo número de sessões é obrigarório.',
                code='required'
            )

        return numero_sessoes

    def clean_numero_tentativas(self):
        numero_tentativas = self.cleaned_data.get('numero_tentativas')
        if numero_tentativas is None or numero_tentativas < 1:
            raise forms.ValidationError(
                'O campo número de tentativas é obrigarório.',
                code='required'
            )

        return numero_tentativas

    def save(self, commit=True):
        programa = super().save(commit=False)
        programa.profissional = self.cleaned_data["profissional"]
        if commit:
            programa.save()
        return programa
