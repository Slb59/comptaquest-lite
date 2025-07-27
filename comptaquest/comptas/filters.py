"""Filter forms used to refine the results displayed to the user.

Contains optional fields allowing you to dynamically filter database objects.
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.utils.translation import gettext_lazy as _

from secretbox.users.models import Member

from .choices import ACCOUNT_CHOICES, BANK_CHOICES


class CurrentAccountFilterForm(forms.Form):

    user = forms.ModelChoiceField(queryset=Member.objects.all(), required=False, label="Propriétaire de compte")
    bank_name = forms.ChoiceField(label=_("Banque"), choices=[("", "Toutes")] + BANK_CHOICES, required=False)
    account_type = forms.ChoiceField(label=_("Type de compte"), choices=ACCOUNT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "p-4 bg-gray-100 rounded mb-4"
        self.helper.label_class = "font-semibold"
        self.helper.field_class = "w-full"
        self.helper.attrs = {
            "id": "current-account-filter-form",
            "novalidate": "novalidate",
            "data-autosubmit": "true",
        }
        self.helper.layout = Layout(
            Row(
                Column("user", css_class="sm:col-span-1"),
                Column("bank_name", css_class="sm:col-span-1"),
                Column("account_type", css_class="sm:col-span-1"),
                css_class="grid grid-cols-3 gap-4",
            ),
        )
