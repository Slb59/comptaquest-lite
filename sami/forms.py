from django import forms
from .models import Sami
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django.utils.translation import gettext_lazy as _

from secretbox.tools.tooltip import TooltipFromInstanceMixin


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
                    Field("bedtime", wrapper_class="col-span-1"),
                    Field("wakeup", wrapper_class="col-span-1"),
                    Field("nonstop", wrapper_class="col-span-1"),
                    Field("energy", wrapper_class="col-span-1"),
                    Field("naptime", wrapper_class="col-span-1"),
                    Field("phone", wrapper_class="col-span-1"),
                    Field("reading", wrapper_class="col-span-1"),
                    css_class="grid grid-cols-7 gap-4 mt-4",
                ),
                css_class="w-full max-w-2xl"         
            )
        )