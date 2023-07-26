from django import forms
from application.models import Profissional
import re

# FORMULÁRIOS PARA A CRIAÇÃO DE USUÁRIO PROFISSIONAL


class RegisterForm(forms.ModelForm):

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
            'placeholder': 'Digite seu nome',
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
            ("Fonoaudiologia", "Fonoaudiologia"),
            ("Neuropsicopedagogia", "Neuropsicopedagogia"),
            ("Pedagogia", "Pedagogia"),
            ("Psicologia", "Psicologia"),
            ("Psicomotricidade", "Psicomotricidade"),
            ("Psicopedagogia", "Psicopedagogia"),
            ("Terapia Ocupacional", "Terapia Ocupacional"),
            ("Outros", "Outros"),

        ],
        widget=forms.Select(
            attrs={
                'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5"  # noqa
            }
        )
    )

    celular = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': "(99) 99999-9999",
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'oninput': "formatarNumeroCelular('id_celular')",
            'autocomplete': "off"
        }))

    pais = forms.ChoiceField(
        required=False,
        disabled=True,
        choices=[("Brasil", "Brasil")],
        widget=forms.Select(
            attrs={
                'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5"  # noqa
            }
        )
    )

    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': "email@exemplo.com",
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'oninput': "validarEmail('email')",
            'autocomplete': "off"
        }))

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "••••••••",
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'autocomplete': "off"
        }))

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "••••••••",
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'autocomplete': "off"
        }))

    class Meta:
        model = Profissional
        fields = ('foto_perfil', 'nome', 'data_nascimento',
                  'especialidade', 'celular', 'pais', 'estado', 'cidade',
                  'email', 'password', 'password2')
        exclude = ('username', 'user_permissions', 'groups', 'is_superuser',
                   'last_login', 'first_name', 'last_name', 'date_joined',
                   'is_active', 'is_staff')

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

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if len(celular) == 0:
            raise forms.ValidationError(
                'O campo celular é obrigarório.',
                code='required'
            )

        padrao = r"\(\d{2}\) \d{5}-\d{4}"

        if not re.match(padrao, celular):
            raise forms.ValidationError(
                'O campo celular tem formato inválido.',
                code='invalid'
            )

        return celular

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado == "null" or len(estado) == 0:
            raise forms.ValidationError(
                'O campo estado é obrigarório.',
                code='required'
            )

        return estado

    def clean_cidade(self):
        cidade = self.cleaned_data.get('cidade')
        if cidade is None or cidade == "Selecione a Cidade" or len(cidade) == 0:  # noqa
            raise forms.ValidationError(
                'O campo cidade é obrigarório.',
                code='required'
            )

        return cidade

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) == 0:
            raise forms.ValidationError(
                'O campo email é obrigarório.',
                code='required'
            )

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) == 0:
            raise forms.ValidationError(
                'O campo senha é obrigarório.',
                code='required'
            )

        if len(password) < 8:
            raise forms.ValidationError(
                'O campo senha requer no mínimo 8 caracteres',
                code='required'
            )

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if len(password2) == 0:
            raise forms.ValidationError(
                'O campo de confirmação de senha é obrigarório.',
                code='required'
            )

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'As senhas não correspondem. Por favor, tente novamente.',
                code='invalid'
            )

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
