from django.urls import path

from .views import (
    AccountCreateView,
    AccountDetailView,
    BalanceSheetView,
    DashboardView,
    MembersView,
    OutgoingsCreateView,
    OutgoingsDetailView,
    OutgoingsView,
    TransactionCreateView,
    TransactionDetailView,
    TransactionsView,
)

app_name = "comptas"

urlpatterns = [
    path ("", DashboardView.as_view(), name="dashboard"),
    path("members/", MembersView.as_view(), name="members"),
    # account urls
    path("account/<int:account_id>/", AccountDetailView.as_view(), name="account_detail"),  # for individual accounts
    path("account/create/", AccountCreateView.as_view(), name="account_create"),
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
