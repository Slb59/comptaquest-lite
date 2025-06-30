from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import NomadePosition


class EscapeVaultForm(forms.ModelForm):
    class Meta:
        model = NomadePosition
        fields = [
            "name", "category", "city",
            "latitude", "longitude", "link_to_site",
            "opening_date", "closing_date",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = _("Nom de la position")
        self.fields["category"].label = _("Catégorie")
        self.fields["city"].label = _("Ville")
        self.fields["latitude"].label = _("Latitude")
        self.fields["longitude"].label = _("Longitude")
        self.fields["link_to_site"].label = _("Lien vers le site internet")
        self.fields["opening_date"].label = _("Date d'ouverture")
        self.fields["closing_date"].label = _("Date de fermeture")

        # Redimensionner le champ city
        self.fields["city"].widget.attrs.update({"class": "h-full sm:h-[40px]", "style": "max-height: 40px;"})

        # Redimensionner le champ latitude
        self.fields["latitude"].widget.attrs.update({"class": "w-full sm:w-[170px]", "style": "max-width: 170px;"})

        # Redimensionner le champ longitude
        self.fields["longitude"].widget.attrs.update({"class": "w-full sm:w-[170px]", "style": "max-width: 170px;"})

        self.helper = FormHelper()
        self.helper.form_class = "border p-8"

        self.helper.layout = Layout(
            "name",
            "category",
            "city",
            Div(
                Div("latitude", css_class="w-full sm:w-[170px]"),
                Div("longitude", css_class="w-full sm:w-[170px]"),
                css_class="flex items-center gap-4",
            ),
            "link_to_site",
            Div(
                Div("opening_date", css_class="w-full sm:w-[170px]"),
                Div("closing_date", css_class="w-full sm:w-[170px]"),
                css_class="flex items-center gap-4",
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
