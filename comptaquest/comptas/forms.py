"""Définit les formulaires basés sur les modèles de l'application.

Utilisés pour la création et la mise à jour des objets via des vues
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from comptaquest.comptas.models import (
    CurrentAccount,
    ExpenseTransaction,
    InvestmentAccount,
    Outgoings,
)
from secretbox.tools.tooltip import TooltipFromInstanceMixin

from .choices import ACCOUNT_CHOICES


class SelectAccountTypeForm(forms.Form):
    account_type = forms.ChoiceField(label="Type de compte", choices=ACCOUNT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "mt-4"
        self.helper.add_input(
            Submit(
                "submit",
                "Suivant",
                css_class="button-valider",
            )
        )


class CurrentAccountForm(forms.ModelForm, TooltipFromInstanceMixin):
    class Meta:
        model = CurrentAccount
        exclude = ["account_type", "created_at", "created_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_tooltips_from_instance()
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "mt-4"
        self.helper.label_class = "font-semibold"
        # self.helper.field_class = "w-auto"

        # Resize fields
        self.fields["user"].label = _("Propriétaire de compte")
        # self.fields["user"].widget.attrs.update({"class": "w-full sm:w-[90px]", "style": "max-width: 100px;"})
        print("Champs disponibles :", list(self.fields.keys()))
        self.fields["name"].label = _("Libellé de compte")
        self.fields["bank_name"].label = _("Banque")
        self.fields["pointed_date"].label = _("Dernier pointage")

        self.helper.layout = Layout(
            Div(
                Div(
                    Div("name", css_class="sm:col-span-2"),
                    css_class="grid sm:grid-cols-2 gap-4 mb-4 mt-4",
                ),
                Div(
                    Div("user", css_class="sm:col-span-1"),
                    Div("bank_name", css_class="sm:col-span-1"),
                    css_class="grid sm:grid-cols-2 gap-4 mb-4 mt-4",
                ),
                Div(
                    Div("pointed_date", css_class="sm:col-span-1"),
                    Div("current_balance", css_class="sm:col-span-1"),
                    css_class="grid sm:grid-cols-2 gap-4 mb-4",
                ),
                Div(
                    Div("current_pointed_date", css_class="sm:col-span-1"),
                    Div("current_pointed_balance", css_class="sm:col-span-1"),
                    css_class="grid sm:grid-cols-2 gap-4 mb-4",
                ),
                "average_interest",
                "ledger_analysis",
                Div(
                    Div("state", css_class="sm:col-span-1"),
                    Div("created_date", css_class="sm:col-span-1"),
                    Div("closed_date", css_class="sm:col-span-1"),
                    css_class="grid grid-cols-3 gap-4",
                ),
                "description",
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
                ),
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
