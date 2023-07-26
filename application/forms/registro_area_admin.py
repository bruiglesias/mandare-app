from django.contrib.auth.forms import UserCreationForm
from application.models import Profissional

# FORMULÁRIOS PARA A CRIAÇÃO DE USUÁRIO NA ÁREA ADMINISTRATIVA


class CustomProfissionalCreateForm(UserCreationForm):
    fields = ('first_name', 'last_name', 'fone')

    class Meta:
        model = Profissional
        labels = {'username': 'Username/E-mail'}
        fields = ('first_name', 'last_name', 'celular')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user
