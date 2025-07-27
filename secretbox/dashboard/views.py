from datetime import date

# from crispy_forms.layout import Field
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, View

from .forms import ContactForm, TodoFilterForm, TodoForm
from .models import Todo


class ContactFormView(LoginRequiredMixin, FormView):
    form_class = ContactForm
    template_name = "dashboard/contact.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Contact")
        context["logo_url"] = "/static/images/secretbox/logo_sb2.png"
        return context


@login_required
@require_GET
def check_todo_state(request, pk):
    print("check")
    todo = get_object_or_404(Todo, pk=pk, user=request.user)

    if todo.state in ("done", "cancel"):
        return JsonResponse(
            {"can_validate": False, "message": _("Cette tâche est déjà terminée ou annulée.")}, status=400
        )

    return JsonResponse({"can_validate": True})


@login_required
@require_POST
def todo_mark_done(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)

    success = todo.check_if_state_is_cancel_or_done()

    if not success:
        return JsonResponse({"success": False, "message": _("Cette tâche est déjà terminée ou annulée.")}, status=400)

    new_date_str = request.POST.get("new_date")

    if not new_date_str:
        return JsonResponse({"success": False, "message": _("Date manquante.")}, status=400)
    new_date = parse_date(new_date_str)
    if not new_date:
        return JsonResponse({"success": False, "message": _("Date invalide.")}, status=400)

    success, message = todo.validate_element(new_date)

    if success:
        return JsonResponse({"success": True, "done_date": todo.done_date.strftime("%Y-%m-%d")})
    else:
        return JsonResponse({"success": False, "message": message})


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = "dashboard/add_todo.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Nouvelle entrée")
        context["logo_url"] = "/static/images/secretbox/logo_sb2.png"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def apply_filters(self, todos, data):
        """Apply filters to the queryset"""

        simple_filters = {
            "state": "state",
            "category": "category",
            "priority": "priority",
            "description": lambda v: {"description__icontains": v},
            "appointment": "appointment",
            "who": "who",
            "place": "place",
            "periodic": "periodic",
            "done_date_isnull": lambda v: {"done_date__isnull": v},
        }

        for field, target in simple_filters.items():
            value = data.get(field)
            if value:
                if callable(target):
                    todos = todos.filter(**target(value))
                else:
                    todos = todos.filter(**{target: value})

        range_filters = {
            "planned_date_start": ("planned_date__gte", "planned_date_start"),
            "planned_date_end": ("planned_date__lte", "planned_date_end"),
            "duration_min": ("duration__gte", "duration_min"),
            "duration_max": ("duration__lte", "duration_max"),
            "done_date_start": ("done_date__gte", "done_date_start"),
            "done_date_end": ("done_date__lte", "done_date_end"),
        }

        for field, (lookup, data_key) in range_filters.items():
            value = data.get(data_key)
            if value is not None:
                todos = todos.filter(**{lookup: value})
                if "done_date" in lookup:
                    todos = todos.exclude(done_date__isnull=True)

        return todos

    def get_queryset_by_rights(self, user):
        """Filtrage selon les droits"""
        if user.is_superuser:
            return Todo.objects.all()
        return Todo.objects.filter(Q(user=user) | Q(who=user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TodoFilterForm(self.request.GET or None)
        user = self.request.user
        todos = self.get_queryset_by_rights(user)

        if form.is_valid():
            todos = self.apply_filters(todos, form.cleaned_data)

        context.update(
            {
                "title": _("Bienvenue dans SecretBox"),
                "logo_url": "/static/images/secretbox/logo_sb2.png",
                "todos": todos.order_by("planned_date", "priority", "category", "periodic", "who", "place", "duration"),
                "form": form,
                "request": self.request,
            }
        )

        return context


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = "dashboard/add_todo.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(Q(user=user) | Q(who=user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Modifier l'entrée")
        context["logo_url"] = "/static/images/secretbox/logo_sb2.png"
        return context

    def dispatch(self, request, *args, **kwargs):
        todo = self.get_object()
        if not todo.can_view(request.user):
            return HttpResponseForbidden(_("Vous ne pouvez pas voir cet élément."))

        if not (todo.can_edit(request.user) or todo.can_edit_limited(request.user)):
            return HttpResponseForbidden(_("Vous ne pouvez pas modifier cet élément."))

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # pour le formulaire
        return kwargs


class TodoDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=pk)
        if todo.state != "cancel":
            todo.state = "cancel"
            todo.note = f"*** supprimé {date.today()} ***\n{todo.note}"
            todo.save()
        return redirect("home")

    def dispatch(self, request, *args, **kwargs):
        todo = self.get_object()
        if not todo.can_delete(request.user):
            return HttpResponseForbidden(_("Vous ne pouvez pas supprimer cet élément."))
        return super().dispatch(request, *args, **kwargs)
