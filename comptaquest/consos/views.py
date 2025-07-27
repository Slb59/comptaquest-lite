from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from secretbox.users.mixins import GroupRequiredMixin

GroupRequiredMixin.group_name = "comptas_access"


class ConsosWaterView(LoginRequiredMixin, ListView, GroupRequiredMixin):
    template_name = "consos_water.html"


class ConsosEdfView(LoginRequiredMixin, ListView, GroupRequiredMixin):
    template_name = "consos_edf.html"


class ConsosEdfCreateView(LoginRequiredMixin, CreateView, GroupRequiredMixin):
    template_name = "consos_edf_create.html"


class ConsosWaterCreateView(LoginRequiredMixin, CreateView, GroupRequiredMixin):
    template_name = "consos_water_create.html"


class ConsosEdfDetailView(LoginRequiredMixin, DetailView, GroupRequiredMixin):
    template_name = "consos_edf_detail.html"


class ConsosWaterDetailView(LoginRequiredMixin, DetailView, GroupRequiredMixin):
    template_name = "consos_water_detail.html"
