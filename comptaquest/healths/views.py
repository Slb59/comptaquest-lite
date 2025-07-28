from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from secretbox.users.mixins import GroupRequiredMixin


class ComptasBaseView(LoginRequiredMixin, GroupRequiredMixin):
    group_name = "comptas_access"


class HealthsView(ComptasBaseView, ListView):
    template_name = "healths.html"


class HealthsCreateView(ComptasBaseView, CreateView):
    template_name = "healths_create.html"


class HealthsDetailView(ComptasBaseView, DetailView):
    template_name = "healths_detail.html"
