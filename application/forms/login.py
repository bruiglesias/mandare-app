from django import forms


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': "email@exemplo.com",
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'autocomplete': "off"
        }))

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "••••••••",
            'class': "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5",  # noqa
            'autocomplete': "off"
        }))
