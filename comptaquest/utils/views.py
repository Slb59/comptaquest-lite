from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CategoryListView(LoginRequiredMixin, TemplateView):
    template_name = "categories.html"


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings.html"
