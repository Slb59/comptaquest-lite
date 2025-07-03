from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, FormView, TemplateView,
                                  UpdateView, View)

from .forms import ContactForm, TodoForm, TodoFilterForm
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
        form = TodoFilterForm(self.request.GET or None)
        todos = Todo.objects.filter(user=self.request.user)

        if form.is_valid():
            data = form.cleaned_data
            if data["state"]:
                todos = todos.filter(state=data["state"])
            if data["category"]:
                todos = todos.filter(category=data["category"])
            if data["priority"]:
                todos = todos.filter(priority=data["priority"])
            if data["planned_date_start"]:
                todos = todos.filter(planned_date__gte=data["planned_date_start"])
            if data["planned_date_end"]:
                todos = todos.filter(planned_date__lte=data["planned_date_end"])
            if data["duration_min"] is not None:
                todos = todos.filter(duration__gte=data["duration_min"])
            if data["duration_max"] is not None:
                todos = todos.filter(duration__lte=data["duration_max"])
            if data["description"]:
                todos = todos.filter(description__icontains=data["description"])
            if data["appointment"]:
                todos = todos.filter(appointment=data["appointment"])
            if data["who"]:
                todos = todos.filter(who=data["who"])
            if data["place"]:
                todos = todos.filter(place=data["place"])
            if data["periodic"]:
                todos = todos.filter(periodic=data["periodic"])

        context["title"] = _("Bienvenue dans SecretBox")
        context["logo_url"] = "/static/images/logo_sb.png"
        
        context["todos"] = todos.order_by("planned_date", "priority", "category", "periodic", "who", "place", "duration")
        context["form"] = form
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
