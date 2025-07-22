from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Layout, Row, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import NomadePosition


class EscapeVaultFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=[("", "Toutes")] + NomadePosition.CATEGORY_CHOICES, required=False, label=_("Catégorie")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "p-4 rounded mb-4"
        self.helper.label_class = "font-semibold"
        self.helper.field_class = "w-full"
        self.helper.attrs = {
            "id": "ev-filter-form",
            "novalidate": "novalidate",
            "data-autosubmit": "true",
        }

        self.helper.layout = Layout(
            Row(
                Column("category", css_class="sm:col-span-1"),
                css_class="grid grid-cols-5 gap-4",
            ),
        )


class EscapeVaultForm(forms.ModelForm):
    new_review = forms.CharField(
        label=_("Ajouter un avis"),
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    class Meta:
        model = NomadePosition
        fields = [
            "name",
            "category",
            "city",
            "country",
            "latitude",
            "longitude",
            "link_to_site",
            "opening_date",
            "closing_date",
            "stars",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = _("Nom de la position")
        self.fields["stars"].label = _("Etoiles")
        self.fields["category"].label = _("Catégorie")
        self.fields["city"].label = _("Ville")
        self.fields["country"].label = _("Pays")
        self.fields["latitude"].label = _("Latitude")
        self.fields["longitude"].label = _("Longitude")
        self.fields["link_to_site"].label = _("Lien vers le site internet")
        self.fields["opening_date"].label = _("Date d'ouverture")
        self.fields["closing_date"].label = _("Date de fermeture")

        # Resize the city and country field
        self.fields["city"].widget.attrs.update({"class": "h-full sm:h-[60px]", "style": "max-height: 40px;"})

        self.fields["country"].widget.attrs.update({"class": "h-full sm:h-[60px]", "style": "max-height: 40px;"})

        self.helper = FormHelper()
        self.helper.form_class = "border p-8"

        self.helper.layout = Layout(
            Div(
                Div("name", css_class="w-full sm:col-span-3"),
                Div("stars", css_class="w-full sm:col-span-1"),
                Div("category", css_class="w-full sm:col-span-2"),
                css_class="grid grid-cols-6 gap-4",
            ),
            # "category",
            Div(
                Div("city", css_class="w-full sm:sm:col-span-3"),
                Div("country", css_class="w-full sm:col-span-2"),
                css_class="grid grid-cols-5 gap-4",
            ),
            Div(
                Div("latitude", css_class="w-full sm:col-span-2"),
                Div("longitude", css_class="w-full sm:col-span-2"),
                css_class="grid grid-cols-5 gap-4",
            ),
            "link_to_site",
            Div(
                Div("opening_date", css_class="w-full sm:col-span-2"),
                Div("closing_date", css_class="w-full sm:col-span-2"),
                css_class="grid grid-cols-5 gap-4",
            ),
            Div(
                Submit(
                    "submit",
                    "Valider",
                    css_class="button-valider",
                ),
                HTML(
                    '<a href="{% url \'escapevault:list_positions\' %}" class="inline-block mt-4 focus:outline-none text-white bg-gray-500 hover:bg-gray-700 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:focus:ring-gray-900">Liste</a>'
                ),
                css_class="flex space-x-4",
            ),
        )

        # Insert the new_review field at the end of the form, just before the submit button
        self.helper.layout.fields.insert(-1, "new_review")
