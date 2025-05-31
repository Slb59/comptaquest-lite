from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView


class StartPerformanceView(LoginRequiredMixin, DetailView):
    template_name = "start_performance.html"
