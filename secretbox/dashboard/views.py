from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .models import Todo


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Bienvenue dans votre secretbox")
        context["logo_url"] = "/static/images/logo-sb.png"
        context["todos"] = Todo.objects.filter(user=self.request.user).order_by(
            "date", "priority", "category", "periodic", "who", "place", "duration", "?"
        )[:10]
        return context
