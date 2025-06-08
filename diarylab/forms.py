from django import forms
from .models import DiaryEntry
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['date', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "border p-8"

        self.helper.layout = Layout(
            "date",
            "content",
            Submit(
                "submit",
                "valider",
                css_class="mt-4 focus:outline-none text-white bg-brown hover:bg-darkbrown focus:ring-4 focus:ring-yellow-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:focus:ring-yellow-900",
            ),
        )



