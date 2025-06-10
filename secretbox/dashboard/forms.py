from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms


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
