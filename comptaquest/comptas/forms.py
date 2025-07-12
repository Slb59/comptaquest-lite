from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django import forms

from comptaquest.comptas.models import (CurrentAccount, ExpenseTransaction,
                                        InvestmentAccount, Outgoings)


class SelectAccountTypeForm(forms.Form):
    ACCOUNT_CHOICES = [("Current", "Compte courant"), ("Investment", "Compte d'investissement")]
    account_type = forms.ChoiceField(label="Type de compte", choices=ACCOUNT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Suivant", css_class="button-valider",))


class CurrentAccountForm(forms.ModelForm):
    class Meta:
        model = CurrentAccount
        exclude = ["account_type", "created_at", "created_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Div(
                Submit(
                    "submit",
                    "Valider",
                    css_class="button-valider",
                ),
                HTML(
                    '<a href="{% url \'comptas:dashboard\' %}" class="inline-block mt-4 focus:outline-none text-white bg-gray-500 hover:bg-gray-700 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:focus:ring-gray-900">Liste</a>'
                ),
                css_class="flex space-x-4",
            )
        )


class InvestmentAccountForm(forms.ModelForm):
    class Meta:
        model = InvestmentAccount
        exclude = ["user", "account_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Div(
                Submit(
                    "submit",
                    "Valider",
                    css_class="button-valider",
                ),
                HTML(
                    '<a href="{% url \'comptas:dashboard\' %}" class="inline-block mt-4 focus:outline-none text-white bg-gray-500 hover:bg-gray-700 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:focus:ring-gray-900">Liste</a>'
                ),
                css_class="flex space-x-4",
            )
        )


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
