from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView


class ConsosWaterView(LoginRequiredMixin, ListView):
    template_name = "consos_water.html"


class ConsosEdfView(LoginRequiredMixin, ListView):
    template_name = "consos_edf.html"


class ConsosEdfCreateView(LoginRequiredMixin, CreateView):
    template_name = "consos_edf_create.html"


class ConsosWaterCreateView(LoginRequiredMixin, CreateView):
    template_name = "consos_water_create.html"


class ConsosEdfDetailView(LoginRequiredMixin, DetailView):
    template_name = "consos_edf_detail.html"


class ConsosWaterDetailView(LoginRequiredMixin, DetailView):
    template_name = "consos_water_detail.html"
