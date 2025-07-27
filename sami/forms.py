"""Defines forms based on the application's templates.

Used for creating and updating objects via views
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout
from django import forms
from django.utils.translation import gettext_lazy as _

from secretbox.tools.tooltip import TooltipFromInstanceMixin

from .models import Sami


class SamiForm(forms.ModelForm, TooltipFromInstanceMixin):

    class Meta:
        model = Sami
        exclude = [""]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_tooltips_from_instance()

        self.helper = FormHelper()
        self.helper.form_class = "mt-8"

        self.fields["weight"].label = _("Poids")

        self.helper.layout = Layout(
            Div(
                Div(
                    Field("date", wrapper_class="col-span-1"),
                    Field("weight", wrapper_class="col-span-1"),
                    css_class="grid grid-cols-2 gap-4",
                ),
                Div(
                    Field("bedtime", wrapper_class="col-span-1", attrs={"min": 0, "max": 3}, css_class="w-full"),
                    Field("wakeup", wrapper_class="col-span-1", css_class="w-full"),
                    Field("nonstop", wrapper_class="col-span-1", css_class="w-full"),
                    Field("energy", wrapper_class="col-span-1", css_class="w-full"),
                    Field("naptime", wrapper_class="col-span-1", css_class="w-full"),
                    Field("phone", wrapper_class="col-span-1", css_class="w-full"),
                    Field("reading", wrapper_class="col-span-1", css_class="w-full"),
                    HTML(
                        '<div class="col-span-2 pt-2 w-full text-center"><label>Total Sommeil</label><div id="total-sleep" class="text-lg text-center font-semibold">0</div></div>'
                    ),
                    css_class="grid grid-cols-9 gap-4 mt-4 min-w-0",
                ),
                css_class="w-full max-w-4xl",
            )
        )
