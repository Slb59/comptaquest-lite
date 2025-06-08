from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy

from .models import Todo
from .forms import ContactForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Bienvenue dans SecretBox")
        context["logo_url"] = "/static/images/logo_sb.png"
        context["todos"] = Todo.objects.filter(user=self.request.user).order_by(
            "date", "priority", "category", "periodic", "who", "place", "duration", "?"
        )[:10]
        return context

class ContactFormView(LoginRequiredMixin, FormView):
    form_class = ContactForm
    template_name = "dashboard/contact.html"
    success_url = reverse_lazy("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Contact")
        context["logo_url"] = "/static/images/logo_sb.png"
        return context