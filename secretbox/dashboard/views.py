from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, FormView, TemplateView,
                                  UpdateView, View)

from .forms import ContactForm, TodoForm
from .models import Todo


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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Bienvenue dans SecretBox")
        context["logo_url"] = "/static/images/logo_sb.png"
        context["todos"] = Todo.objects.filter(user=self.request.user).order_by(
            "planned_date", "priority", "category", "periodic", "who", "place", "duration", "?"
        )
        return context


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "dashboard/add_todo.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Nouvelle entrée")
        context["logo_url"] = "/static/images/logo_sb.png"
        return context


class TodoDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=pk)
        if todo.state != "cancel":
            todo.state = "cancel"
            todo.note = f"*** supprimé {date.today()} ***\n{todo.note}"
            todo.save()
        return redirect("home")
