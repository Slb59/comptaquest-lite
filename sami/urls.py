from django.urls import path

from .views import SamiDashboardView, SamiListView, SamiCreateView

app_name = "sami"

urlpatterns = [
    path("dashboard/", SamiDashboardView.as_view(), name="dashboard"),
    path("list/", SamiListView.as_view(), name="list_sami"),
    path("add/", SamiCreateView.as_view(), name="add_sami"),
]
