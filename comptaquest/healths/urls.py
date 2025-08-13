from django.urls import path

from .views import HealthsCreateView, HealthsDetailView, HealthsView

app_name = "healths"

urlpatterns = [
    path("healths/", HealthsView.as_view(), name="healths"),
    path("healths/create/", HealthsCreateView.as_view(), name="healths_create"),
    path(
        "healths/<int:account_id>/", HealthsDetailView.as_view(), name="healths_detail"
    ),
]
