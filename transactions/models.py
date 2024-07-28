# transactions/models.py

from django.db import models
from accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE_CHOICES, DEPOSIT, WITHDRAWAL, TRANSFER

class Transaction(models.Model):
    account = models.ForeignKey(
        UserBankAccount,
        related_name='transactions',
        on_delete=models.CASCADE,
    )
    receiver_account = models.ForeignKey(
        UserBankAccount,
        related_name='received_transactions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} de {self.amount} da conta {self.account} para a conta {self.receiver_account if self.receiver_account else 'N/A'}"

    def get_transaction_description(self):
        if self.transaction_type == DEPOSIT:
            return 'Depósito'
        elif self.transaction_type == WITHDRAWAL:
            return 'Saque'
        elif self.transaction_type == TRANSFER:
            if self.account == self.receiver_account:
                return 'Transferência'
            elif self.receiver_account:
                if self.account == self.receiver_account:
                    return 'Transação Recebida'
                else:
                    return 'Transação Enviada'
            return 'Transferência'
        return 'Transação'

    class Meta:
        ordering = ['timestamp']