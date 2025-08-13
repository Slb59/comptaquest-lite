"""Views for the comptaquest.consos application.
Dashboard, edit, create, delete, and list views.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from secretbox.users.mixins import GroupRequiredMixin


class ComptasBaseView(LoginRequiredMixin, GroupRequiredMixin):
    group_name = "comptas_access"


class ConsosWaterView(ComptasBaseView, ListView):
    template_name = "consos_water.html"


class ConsosEdfView(ComptasBaseView, ListView):
    template_name = "consos_edf.html"


class ConsosEdfCreateView(ComptasBaseView, CreateView):
    template_name = "consos_edf_create.html"


class ConsosWaterCreateView(ComptasBaseView, CreateView):
    template_name = "consos_water_create.html"


class ConsosEdfDetailView(ComptasBaseView, DetailView):
    template_name = "consos_edf_detail.html"


class ConsosWaterDetailView(ComptasBaseView, DetailView):
    template_name = "consos_water_detail.html"
