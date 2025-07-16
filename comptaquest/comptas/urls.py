from django.urls import path

from .views import (
    AccountCreateView, AccountTypeSelectView,
    AccountEditView, AccountDeleteView,
    BalanceSheetView,
    DashboardView, OutgoingsCreateView, OutgoingsDetailView,
    OutgoingsView, TransactionCreateView,
    TransactionDetailView, TransactionsView
)

app_name = "comptas"

urlpatterns = [
    path("account/", DashboardView.as_view(), name="dashboard"),
    path("account/new/", AccountTypeSelectView.as_view(), name="account-select"),
    path("account/create/", AccountCreateView.as_view(), name="account-create"),
    path("<int:pk>/edit/", AccountEditView.as_view(), name="edit_account"),
    path("<int:pk>/delete/", AccountDeleteView.as_view(), name="delete_account"),

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
