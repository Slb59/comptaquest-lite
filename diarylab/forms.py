"""Définit les formulaires basés sur les modèles de l'application.

Utilisés pour la création et la mise à jour des objets via des vues
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms

from secretbox.tools.form_helpers import action_buttons

from .models import DiaryEntry


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ["date", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["content"].label = "La pensée du jour"

        self.helper = FormHelper()
        self.helper.form_class = "border p-8"

        self.helper.layout = Layout(
            "date",
            "content",
            action_buttons(back_url_name="diarylab:list_entries", back_label="Liste"),
        )
