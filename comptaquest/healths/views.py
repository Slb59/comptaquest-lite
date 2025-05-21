from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView


class HealthsView(LoginRequiredMixin, ListView):
    template_name = "healths.html"


class HealthsCreateView(LoginRequiredMixin, CreateView):
    template_name = "healths_create.html"


class HealthsDetailView(LoginRequiredMixin, DetailView):
    template_name = "healths_detail.html"
