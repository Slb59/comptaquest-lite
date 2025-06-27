from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, DeleteView

from .forms import ContactForm, TodoForm
from .models import Todo


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Bienvenue dans SecretBox")
        context["logo_url"] = "/static/images/logo_sb.png"
        context["todos"] = Todo.objects.filter(user=self.request.user).order_by(
            "planned_date", "priority", "category", "periodic", "who", "place", "duration", "?"
        )[:10]
        return context


class ContactFormView(LoginRequiredMixin, FormView):
    form_class = ContactForm
    template_name = "dashboard/contact.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Contact")
        context["logo_url"] = "/static/images/logo_sb.png"
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = "dashboard/add_todo.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Nouvelle entrée")
        context["logo_url"] = "/static/images/logo_sb.png"
        return context

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "dashboard/add_todo.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Nouvelle entrée")
        context["logo_url"] = "/static/images/logo_sb.png"
        return context

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.state = "cancel"
        self.object.note = f"*** supprimé {date.today()} ***\n{self.object.note}"
        self.object.save()
        return super().form_valid(form)