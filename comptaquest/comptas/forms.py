from django import forms

from comptaquest.comptas.models import (CurrentAccount, ExpenseTransaction,
                                        Outgoings, Wallet)


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['name', 'label', 'amount']


class CurrentAccountForm(forms.ModelForm):
    class Meta:
        model = CurrentAccount
        fields = ["name", "description"]


class OutgoingsForm(forms.ModelForm):
    class Meta:
        model = Outgoings
        fields = [
            "name",
            "description",
            "amount",
            "periodicity",
            "start_date",
            "end_date",
        ]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = ExpenseTransaction
        fields = ["description", "amount", "date_pointed"]
