from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, UserBankAccount
from .constants import GENDER_CHOICE
from django.contrib.auth.forms import AuthenticationForm


class UserRegistrationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICE, label="Gênero")
    birth_date = forms.DateField(label="Data de Nascimento", widget=forms.DateInput(format='%d/%m/%Y'), input_formats=['%d/%m/%Y'])
    cpf = forms.CharField(max_length=11, label="CPF")

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'cpf',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['first_name'].label = "Nome"
        self.fields['last_name'].label = "Sobrenome"
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirme a Senha"
        self.fields['cpf'].label = "CPF"
        self.fields['birth_date'].widget.attrs['placeholder'] = 'DD/MM/YYYY'

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            cpf = self.cleaned_data.get('cpf')

            UserBankAccount.objects.create(
                user=user,
                gender=gender,
                birth_date=birth_date,
                cpf=cpf,
            )
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': (
            'appearance-none block w-full bg-gray-200 '
            'text-gray-700 border border-gray-200 '
            'rounded py-3 px-4 leading-tight '
            'focus:outline-none focus:bg-white '
            'focus:border-gray-500'
        )
    }))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={
        'class': (
            'appearance-none block w-full bg-gray-200 '
            'text-gray-700 border border-gray-200 '
            'rounded py-3 px-4 leading-tight '
            'focus:outline-none focus:bg-white '
            'focus:border-gray-500'
        )
    }))