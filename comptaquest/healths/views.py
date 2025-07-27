from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from secretbox.users.mixins import GroupRequiredMixin

GroupRequiredMixin.group_name = "comptas_access"


class HealthsView(LoginRequiredMixin, ListView, GroupRequiredMixin):
    template_name = "healths.html"


class HealthsCreateView(LoginRequiredMixin, CreateView, GroupRequiredMixin):
    template_name = "healths_create.html"


class HealthsDetailView(LoginRequiredMixin, DetailView, GroupRequiredMixin):
    template_name = "healths_detail.html"
