from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from secretbox.users.mixins import GroupRequiredMixin

GroupRequiredMixin.group_name = "comptas_access"

class CategoryListView(LoginRequiredMixin, TemplateView, GroupRequiredMixin):
    template_name = "categories.html"


class SettingsView(LoginRequiredMixin, TemplateView, GroupRequiredMixin):
    template_name = "settings.html"
