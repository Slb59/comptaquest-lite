from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django import forms

from .models import Todo


class ContactForm(forms.Form):
    REASON_CHOICES = [
        ("", "Select a reason"),
        ("general", "General Inquiry"),
        ("support", "Technical Support"),
        ("feedback", "Feedback"),
        ("other", "Other"),
    ]
    name = forms.CharField(label="Your Name", max_length=100, required=True)
    email = forms.EmailField(label="Your Email", required=True)
    reason = forms.ChoiceField(label="Reason for Contact", choices=REASON_CHOICES, required=True)
    subject = forms.CharField(label="Subject", max_length=200, required=False)
    message = forms.CharField(label="Your Message", widget=forms.Textarea(attrs={"rows": 4}), required=True)
    subscribe = forms.BooleanField(label="Subscribe to newsletter", required=False)

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
        self.fields["appointment"].label = "Date et heure"
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
