"""Views for the samicheck application.
Dashboard, edit, create, delete, and list views.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, TemplateView

from secretbox.users.mixins import GroupRequiredMixin

from .forms import SamiForm
from .models import Sami


class ComptasBaseView(LoginRequiredMixin, GroupRequiredMixin):
    group_name = "sami_access"


class SamiDashboardView(ComptasBaseView, TemplateView):

    template_name = "sami/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("SamiCheck")
        context["logo_url"] = "/static/images/logo_sami.png"
        return context


class SamiListView(ComptasBaseView, ListView):
    model = Sami
    template_name = "sami/list.html"
    context_object_name = "samis"

    def get_queryset(self):
        return Sami.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Tableau Sami")
        context["logo_url"] = "/static/images/logo_sami.png"
        return context


class SamiCreateView(ComptasBaseView, CreateView):
    model = Sami
    form_class = SamiForm
    template_name = "sami/add_sami.html"
    success_url = reverse_lazy("sami:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Ajouter un nouveau Sami")
        context["logo_url"] = "/static/images/logo_sami.png"
        return context
