from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit, Row, Column
from django import forms
from django.utils.translation import gettext_lazy as _

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
    subscribe =forms.BooleanField(label=_("Souscris à ma newsletter"), required=False)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["state"].label = "État"
        self.fields["duration"].label = "Durée"
        self.fields["description"].label = "Description"
        self.fields["appointment"].label = "Rdv"
        self.fields["category"].label = "Catégorie"
        self.fields["who"].label = "Personne"
        self.fields["place"].label = "Lieu"
        self.fields["periodic"].label = "Fréquence"

        # Resize the state field
        self.fields["state"].widget.attrs.update({"class": "w-full sm:w-[150px]", "style": "max-width: 150px;"})

        # Resize the duration field
        self.fields["duration"].widget.attrs.update({"class": "w-full sm:w-[90px]", "style": "max-width: 90px;"})

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


class TodoFilterForm(forms.Form):
    state = forms.ChoiceField(
        choices=[("", "Tous")] + Todo.STATE_CHOICES,
        required=False,
        label="Etat"
    )
    duration_min = forms.IntegerField(required=False, min_value=0, label="Durée min")
    duration_max = forms.IntegerField(required=False, min_value=0, label="Durée max")
    description = forms.CharField(required=False)
    appointment = forms.ChoiceField(choices=[("", "Tous")] + Todo.APPOINTEMENT_CHOICES, required=False, label=_("Rendez-vous"))
    category = forms.ChoiceField(
        choices=[("", "Toutes")] + Todo.CATEGORY_CHOICES,
        required=False,
        label = _("Catégorie")
    )
    who = forms.ChoiceField(
        choices=[("", "Toutes")] + Todo.WHO_CHOICES,
        required=False,
        label=_("Qui"))
    place = forms.ChoiceField(
        choices=[("", "Toutes")] + Todo.PLACE_CHOICES,
        required=False,
        label = _("Lieu"))
    periodic = forms.ChoiceField(
        choices=[("", "Toutes")] + Todo.PERIODIC_CHOICES,
        required=False,
        label=_("Fréquence"))    
    planned_date_start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Date de planification"))
    planned_date_end = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("_"))
    priority = forms.ChoiceField(
        choices=[("", "Toutes")] + Todo.PRIORITY_CHOICES,
        required=False,
        label=_("Priorité"))
    done_date_start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("Date de fin"))
    done_date_end = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label=_("_"))
    note = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "p-4 bg-gray-100 rounded mb-4"
        self.helper.label_class = "font-semibold"
        self.helper.field_class = "w-full"
        self.helper.attrs = {
            "id": "todo-filter-form",
            "novalidate": "novalidate",
        }

        self.helper.layout = Layout(
            Row(
                Column("state", css_class="sm:col-span-1"),
                Column("duration_min", css_class="sm:col-span-1"),
                Column("duration_max", css_class="sm:col-span-1"),
                Column("description", css_class="sm:col-span-3"),
                Column("appointment", css_class="sm:col-span-1"),
                Column("category", css_class="sm:col-span-1"),
                Column("who", css_class="sm:col-span-1"),
                Column("place", css_class="sm:col-span-1"),
                Column("periodic", css_class="sm:col-span-1"),
                css_class="grid grid-cols-11 gap-4",
            ),
            Row(                
                Column("planned_date_start", css_class="sm:col-span-1"),
                Column("planned_date_end", css_class="sm:col-span-1"),   
                Column("priority", css_class="sm:col-span-1"), 
                Column("done_date_start", css_class="sm:col-span-1"),
                Column("done_date_end", css_class="sm:col-span-1"),
                css_class="grid grid-cols-5 gap-4 py-2",
            ),
            # Submit("submit", "Filtrer", css_class="bg-blue-500 text-white px-4 py-2 rounded"),
        )

    
