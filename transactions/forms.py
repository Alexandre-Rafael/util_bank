# transactions/forms.py

import datetime
from django import forms
from django.conf import settings
from .models import Transaction
from accounts.models import UserBankAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = settings.MINIMUM_DEPOSIT_AMOUNT
        amount = self.cleaned_data.get('amount')

        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'Você precisa depositar pelo menos {min_deposit_amount} R$'
            )

        return amount


class WithdrawForm(TransactionForm):
    def clean_amount(self):
        min_withdraw_amount = settings.MINIMUM_WITHDRAWAL_AMOUNT
        balance = self.account.balance

        amount = self.cleaned_data.get('amount')

        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'Você pode sacar pelo menos {min_withdraw_amount} R$'
            )

        if amount > balance:
            raise forms.ValidationError(
                f'Você tem {balance} R$ na sua conta. '
                'Você não pode sacar mais do que o saldo da sua conta'
            )

        return amount


class TransferForm(forms.Form):
    receiver_cpf = forms.CharField(max_length=11, label="CPF do Recebedor")
    amount = forms.DecimalField(decimal_places=2, max_digits=12, label="Quantia")

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        receiver_cpf = cleaned_data.get('receiver_cpf')

        if self.account:
            if amount and amount <= 0:
                self.add_error('amount', 'A quantia deve ser positiva.')
            if receiver_cpf and self.account.cpf == receiver_cpf:
                self.add_error('receiver_cpf', 'Não é possível transferir para a mesma conta.')

        if receiver_cpf:
            try:
                UserBankAccount.objects.get(cpf=receiver_cpf)
            except UserBankAccount.DoesNotExist:
                self.add_error('receiver_cpf', 'A conta do recebedor não existe.')

        return cleaned_data


class TransactionDateRangeForm(forms.Form):
    daterange = forms.CharField(required=False)

    def clean_daterange(self):
        daterange = self.cleaned_data.get("daterange")

        try:
            daterange = daterange.split(' - ')
            if len(daterange) == 2:
                for date in daterange:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                return daterange
            else:
                raise forms.ValidationError("Por favor, selecione um intervalo de datas.")
        except (ValueError, AttributeError):
            raise forms.ValidationError("Intervalo de datas inválido")
