# transactions/urls.py
from django.urls import path
from .views import DepositMoneyView, WithdrawMoneyView, TransactionRepostView, TransferMoneyView

app_name = 'transactions'

urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposit_money'),
    path('withdraw/', WithdrawMoneyView.as_view(), name='withdraw_money'),
    path('report/', TransactionRepostView.as_view(), name='transaction_report'),
    path('transfer/', TransferMoneyView.as_view(), name='transfer_money'),
]
