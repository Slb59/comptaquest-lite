from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, TemplateView

from .models import Sami


class SamiDashboardView(LoginRequiredMixin, TemplateView):

    template_name = "sami/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Tableau Sami")
        context["logo_url"] = "/static/images/logo_sami.png"
        return context


class SamiListView(LoginRequiredMixin, ListView):
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
