from django.urls import path

from .views import (AccountCreateView, AccountDetailView, BalanceSheetView,
                    DashboardView, MembersView, OutgoingsCreateView,
                    OutgoingsDetailView, OutgoingsView, TransactionCreateView,
                    TransactionDetailView, TransactionsView)
from .views import WalletListView, WalletCreateView, WalletUpdateView, WalletDeleteView

app_name = "comptas"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("members/", MembersView.as_view(), name="members"),

    # wallet urls
    path('wallets/', WalletListView.as_view(), name='wallet_list'),
    path('wallets/create/', WalletCreateView.as_view(), name='wallet_create'),
    path('wallets/<str:pk>/update/', WalletUpdateView.as_view(), name='wallet_update'),
    path('wallets/<str:pk>/delete/', WalletDeleteView.as_view(), name='wallet_delete'),

    # outgoings urls
    path("outgoings/", OutgoingsView.as_view(), name="outgoings"),
    path(
        "outgoings/<int:account_id>/",
        OutgoingsDetailView.as_view(),
        name="outgoings_detail",
    ),
    path("outgoings/create/", OutgoingsCreateView.as_view(), name="outgoings_create"),
    # balance sheet urls
    path("balance-sheet/", BalanceSheetView.as_view(), name="balance_sheet"),
    # transaction urls
    path("transactions/", TransactionsView.as_view(), name="transactions"),
    path(
        "transactions/<int:account_id>/",
        TransactionDetailView.as_view(),
        name="transaction_detail",
    ),
    path(
        "transactions/create/",
        TransactionCreateView.as_view(),
        name="transaction_create",
    ),
]
