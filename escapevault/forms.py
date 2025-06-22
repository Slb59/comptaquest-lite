from .models import EscapeVaultPosition
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit

class EscapeVaultPositionForm(forms.ModelForm):
    class Meta:
        model = EscapeVaultPosition
        fields = ["name", "city", "latitude", "longitude"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = _("Nom de la position")
        self.fields["city"].label = _("Ville")
        self.fields["latitude"].label = _("Latitude")
        self.fields["longitude"].label = _("Longitude")

        self.helper = FormHelper()
        self.helper.form_class = "border p-8"

        self.helper.layout = Layout(
            "name",
            "city",
            "latitude",
            "longitude",
            Div(
                Submit(
                    "submit",
                    "Valider",
                    css_class="button-valider",
                    ),
                HTML(
                    '<a href="{% url \'escapevault:list\' %}" class="inline-block mt-4 focus:outline-none text-white bg-gray-500 hover:bg-gray-700 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:focus:ring-gray-900">Liste</a>'
                ),
                css_class="flex space-x-4",
            ),
        )