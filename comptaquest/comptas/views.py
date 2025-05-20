from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView

from .forms import CurrentAccountForm, OutgoingsForm
from .models.account import CurrentAccount
from .models.outgoings import Outgoings
from .models.transaction import Transaction


class DashboardView(LoginRequiredMixin, ListView):
    template_name = "dashboard.html"
    model = CurrentAccount  # for the model to be used in the template
    context_object_name = "accounts"  # for the context variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_date"] = timezone.now()
        context["accounts"] = CurrentAccount.objects.all()
        return context


class MembersView(LoginRequiredMixin, ListView):
    template_name = "members.html"


class AccountDetailView(LoginRequiredMixin, DetailView):
    template_name = "account_detail.html"
    model = CurrentAccount
    context_object_name = "account"


class AccountCreateView(LoginRequiredMixin, CreateView):
    template_name = "account_create.html"
    model = CurrentAccount
    form_class = CurrentAccountForm
    success_url = reverse_lazy("comptas:dashboard")

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # if you need to set the creator
        return super().form_valid(form)


class OutgoingsView(LoginRequiredMixin, ListView):
    template_name = "outgoings.html"
    model = Outgoings
    context_object_name = "outgoings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["outgoings"] = Outgoings.objects.all()
        return context


class OutgoingsDetailView(LoginRequiredMixin, DetailView):
    template_name = "outgoings_detail.html"
    model = Outgoings
    context_object_name = "outgoings"


class OutgoingsCreateView(LoginRequiredMixin, CreateView):
    template_name = "outgoings_create.html"
    model = Outgoings
    form_class = OutgoingsForm
    success_url = reverse_lazy("comptas:outgoings")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BalanceSheetView(LoginRequiredMixin, ListView):
    template_name = "balance_sheet.html"


class TransactionsView(LoginRequiredMixin, ListView):
    template_name = "transactions.html"


class TransactionDetailView(LoginRequiredMixin, DetailView):
    template_name = "transaction_detail.html"
    model = Transaction


class TransactionCreateView(LoginRequiredMixin, CreateView):
    template_name = "transaction_create.html"
    model = Transaction
