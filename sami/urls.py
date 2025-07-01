from .views import SamiDashboardView, SamiListView
from django.urls import path

app_name = "sami"

urlpatterns = [
    path("dashboard/", SamiDashboardView.as_view(), name="dashboard"),
    path("list/", SamiListView.as_view(), name="list"),
]