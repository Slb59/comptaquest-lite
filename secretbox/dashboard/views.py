from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Todo


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Dashboard")
        context["logo_url"] = "/static/images/logo-sb.png"
        context['todos'] = Todo.objects.filter(user=self.request.user).order_by(
            'date', 'priority', 'type', 'periodic', 'who', 'place', 'duration', '?'
        )[:10]
        return context