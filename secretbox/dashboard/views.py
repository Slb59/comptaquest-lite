from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import (CreateView, FormView, TemplateView,
                                  UpdateView, View)
from django.db.models import Q

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TodoFilterForm(self.request.GET or None)
        user = self.request.user
        todos = Todo.objects.filter(user=user)

        # Filtrage selon les droits
        if user.is_superuser:
            todos = Todo.objects.all()
        else:
            todos = Todo.objects.filter(
                Q(user=user) | Q(who=user)
            )

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
            if data["done_date_start"]:
                todos = todos.filter(done_date__gte=data["done_date_start"])
                todos = todos.exclude(done_date__isnull=True)

            if data["done_date_end"]:
                todos = todos.filter(done_date__lte=data["done_date_end"])
                todos = todos.exclude(done_date__isnull=True)

            if data["done_date_isnull"]:
                todos = todos.filter(done_date__isnull=data["done_date_isnull"])

        context["title"] = _("Bienvenue dans SecretBox")
        context["logo_url"] = "/static/images/secretbox/logo_sb2.png"

        context["todos"] = todos.order_by(
            "planned_date", "priority", "category", "periodic", "who", "place", "duration"
        )
        context["form"] = form
        context["request"] = self.request

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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        todo = self.get_object()
        user = self.request.user

        if todo.can_edit_limited(user):
            # Désactive tous les champs sauf statut et priorité
            for name, field in form.fields.items():
                if name not in ["state", "priority"]:
                    field.disabled = True
                    field.widget.attrs.update({"class": "readonly bg-gray-100 text-gray-500 pointer-events-none"}) 
                    
                else:
                    field.widget.attrs.update({"class": "editable"}) 

        return form


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
