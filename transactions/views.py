from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from transactions.constants import DEPOSIT, WITHDRAWAL, TRANSFER
from transactions.forms import DepositForm, WithdrawForm, TransferForm, TransactionDateRangeForm
from transactions.models import Transaction
from django.shortcuts import get_object_or_404
from accounts.models import UserBankAccount


class TransactionRepostView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def get(self, request, *args, **kwargs):
        form = TransactionDateRangeForm(request.GET or None)
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )

        daterange = self.form_data.get("daterange")

        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account,
            'form': TransactionDateRangeForm(self.request.GET or None)
        })

        return context



class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Depositar Dinheiro na Sua Conta'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        if not account.initial_deposit_date:
            now = timezone.now()
            account.initial_deposit_date = now
            account.interest_start_date = now + relativedelta(months=+1)

        account.balance += amount
        account.save(update_fields=['initial_deposit_date', 'balance', 'interest_start_date'])

        messages.success(
            self.request,
            f'R$ {amount} foi depositado na sua conta com sucesso'
        )

        return super().form_valid(form)

class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Sacar Dinheiro da Sua Conta'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        if account.balance < amount:
            messages.error(self.request, 'Fundos insuficientes')
            return self.form_invalid(form)

        account.balance -= amount
        account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'R$ {amount} foi sacado da sua conta com sucesso'
        )

        return super().form_valid(form)

class TransferMoneyView(FormView):
    form_class = TransferForm
    template_name = 'transactions/transfer_form.html'
    success_url = reverse_lazy('transactions:transaction_report')
    title = 'Transferir Dinheiro'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['account'] = self.request.user.account  # Passa a conta do usuário
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        receiver_cpf = form.cleaned_data.get('receiver_cpf')
        from_account = self.request.user.account

        try:
            receiver_account = UserBankAccount.objects.get(cpf=receiver_cpf)
        except UserBankAccount.DoesNotExist:
            messages.error(self.request, 'A conta do recebedor não existe.')
            return self.form_invalid(form)

        if amount > from_account.balance:
            messages.error(self.request, 'Fundos insuficientes.')
            return self.form_invalid(form)

        # Process the transfer
        from_account.balance -= amount
        receiver_account.balance += amount

        from_account.save()
        receiver_account.save()

        # Create transactions
        Transaction.objects.create(
            account=from_account,
            receiver_account=receiver_account,
            amount=-amount,
            balance_after_transaction=from_account.balance,
            transaction_type=TRANSFER
        )
        Transaction.objects.create(
            account=receiver_account,
            receiver_account=receiver_account,
            amount=amount,
            balance_after_transaction=receiver_account.balance,
            transaction_type=TRANSFER
        )

        messages.success(self.request, f'R$ {amount} foi transferido com sucesso')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Houve um erro ao processar sua transferência.')
        return super().form_invalid(form)