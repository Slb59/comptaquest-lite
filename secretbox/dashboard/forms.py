"""Defines forms based on the application's templates.

Used for creating and updating objects via views
"""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from secretbox.users.models import Member

from .models import Todo


class ContactForm(forms.Form):
    REASON_CHOICES = [
        ("", _("Choisis une raison")),
        ("general", _("Demande générale")),
        ("support", _("Support technique")),
        ("feedback", _("Conseil et avis")),
        ("other", _("Autre")),
    ]
    name = forms.CharField(label=_("Ton nom"), max_length=100, required=True)
    email = forms.EmailField(label=_("Ton Email"), required=True)
    reason = forms.ChoiceField(label=_("Pourquoi me contactes-tu ?"), choices=REASON_CHOICES, required=True)
    subject = forms.CharField(label=_("Sujet"), max_length=200, required=False)
    message = forms.CharField(label=_("Ton message"), widget=forms.Textarea(attrs={"rows": 4}), required=True)
    subscribe = forms.BooleanField(label=_("Souscris à ma newsletter"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "border p-8"
        self.helper.layout = Layout(
            "name",
            "email",
            "reason",
            "subject",
            "message",
            "subscribe",
            Submit(
                "submit",
                "Se connecter",
                css_class="button-valider",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get("subject")
        message = cleaned_data.get("message")

        if subject and message:
            if len(subject) < 5:
                self.add_error("subject", "The subject must be at least 5 characters long.")
            if len(message) < 10:
                self.add_error("message", "The message must be at least 10 characters long.")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            "state",
            "duration",
            "description",
            "appointment",
            "category",
            "who",
            "place",
            "periodic",
            "planned_date",
            "priority",
            "note",
        ]

    def __init__(self, *args, user=None, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)

        self.fields["state"].label = "État"
        self.fields["duration"].label = "Durée"
        self.fields["description"].label = "Description"
        self.fields["appointment"].label = "Rdv"
        self.fields["category"].label = "Catégorie"
        self.fields["who"].queryset = Member.objects.order_by("trigram")
        self.fields["who"].label = "Personne"
        self.fields["place"].label = "Lieu"
        self.fields["periodic"].label = "Fréquence"

        # Resize the state field
        # self.fields["state"].widget.field_class="w-full sm:w-[150px]"
        # Field('state', css_id="custom_state_id")
        Field("state", wrapper_class="w-full sm:w-[150px]")
        # Resize the duration field
        Field("state", wrapper_class="w-full sm:w-[90px]")
        self.fields["duration"].widget.field_class = "w-full sm:w-[90px]"

        if instance and user and instance.can_edit_limited(user):
            for name, field in self.fields.items():
                if name not in ["state", "priority"]:
                    field.disabled = True
                    Field(name, wrapper_class="readonly")
                else:
                    Field(name, wrapper_class="editable")

                # for name, field in self.fields.items():

                #     if name not in ["state", "priority"]:
                #         field.disabled = True

                #         field.widget.attrs.update({"class": "readonly text-gray-500 pointer-events-none"})

                #     else:
                #         field.widget.attrs.update({"class": "editable"})

        self.helper = FormHelper()
        self.helper.form_class = "border p-8"
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.attrs = {"novalidate": "novalidate"}

        self.helper.layout = Layout(
            "state",
            "duration",
            "description",
            "appointment",
            "category",
            "who",
            "place",
            "periodic",
            "planned_date",
            "priority",
            "note",
            Div(
                Submit(
                    "submit",
                    "Valider",
                    css_class="button-valider",
                ),
                HTML(
                    '<a href="{% url \'home\' %}" class="inline-block mt-4 focus:outline-none text-white bg-gray-500 hover:bg-gray-700 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:focus:ring-gray-900">Liste</a>'
                ),
                css_class="flex space-x-4",
            ),
        )
