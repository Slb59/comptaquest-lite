import locale
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from secretbox.users.mixins import GroupRequiredMixin

from .choices import ACCOUNT_CHOICES
from .forms import (
    CurrentAccountForm,
    InvestmentAccountForm,
    OutgoingsForm,
    SelectAccountTypeForm,
)
from .filters import CurrentAccountFilterForm
from .models.account import CurrentAccount
from .models.outgoings import Outgoings
from .models.transaction import Transaction


class ComptasBaseView(LoginRequiredMixin, GroupRequiredMixin):
    group_name = "comptas_access"


class DashboardView(ComptasBaseView, TemplateView):
    template_name = "comptaquest/list_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CurrentAccountFilterForm(self.request.GET or None)
        accounts = CurrentAccount.objects.all()

        if form.is_valid():
            data = form.cleaned_data
            if data["user"]:
                accounts = accounts.filter(user=data["user"])
            if data["bank_name"]:
                accounts = accounts.filter(bank_name=data["bank_name"])
            if data["account_type"]:
                accounts = accounts.filter(account_type=data["account_type"])

        try:
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
        except locale.Error:
            pass

        context["title"] = datetime.today().strftime("%A %d %B %Y")
        context["logo_url"] = "/static/images/logo_cq.png"
        context["current_date"] = datetime.today()
        context["accounts"] = accounts.order_by("user", "bank_name", "name")
        context["form"] = form
        return context


class AccountEditView(ComptasBaseView, UpdateView):
    template_name = "account_detail.html"
    model = CurrentAccount
    context_object_name = "account"

    def get_success_url(self):
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return reverse("comptas:dashboard")


class AccountDeleteView(ComptasBaseView, DeleteView):
    template_name = "account_confirm_delete.html"
    model = CurrentAccount
    context_object_name = "account"


class AccountTypeSelectView(FormView, ComptasBaseView):
    template_name = "generic/add_template.html"
    form_class = SelectAccountTypeForm
    success_url = reverse_lazy("comptas:account-create")

    def form_valid(self, form):
        # Stocke le type de compte dans la session
        self.request.session["selected_account_type"] = form.cleaned_data["account_type"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Choix du type de compte")
        context["logo_url"] = "/static/images/logo_cq.png"
        return context


class AccountCreateView(ComptasBaseView, CreateView):
    template_name = "generic/add_template.html"
    success_url = reverse_lazy("comptas:dashboard")

    # model = CurrentAccount
    # form_class = CurrentAccountForm

    def dispatch(self, request, *args, **kwargs):
        # Make sure the account type is set
        self.account_type = request.session.get("selected_account_type")
        if not self.account_type:
            return redirect("comptas:account-select")  # return to the first step
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.account_type == "Current":
            return CurrentAccountForm
        else:
            return InvestmentAccountForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs  # no additional data at this time

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.account_type = self.account_type
        instance.save()
        # clear session after use
        del self.request.session["selected_account_type"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_type_label = dict(ACCOUNT_CHOICES).get(self.account_type, self.account_type)
        context["title"] = _("Nouveau ") + account_type_label.lower()
        context["logo_url"] = "/static/images/logo_cq.png"
        context["account_type"] = self.account_type
        return context


class OutgoingsView(ComptasBaseView, ListView):
    template_name = "outgoings.html"
    model = Outgoings
    context_object_name = "outgoings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["outgoings"] = Outgoings.objects.all()
        return context


class OutgoingsDetailView(ComptasBaseView, DetailView):
    template_name = "outgoings_detail.html"
    model = Outgoings
    context_object_name = "outgoings"


class OutgoingsCreateView(ComptasBaseView, CreateView):
    template_name = "outgoings_create.html"
    model = Outgoings
    form_class = OutgoingsForm
    success_url = reverse_lazy("comptas:outgoings")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BalanceSheetView(ComptasBaseView, ListView):
    template_name = "balance_sheet.html"


class TransactionsView(ComptasBaseView, ListView):
    template_name = "transactions.html"


class TransactionDetailView(ComptasBaseView, DetailView):
    template_name = "transaction_detail.html"
    model = Transaction


class TransactionCreateView(ComptasBaseView, CreateView):
    template_name = "transaction_create.html"
    model = Transaction
