from django.urls import path
from .views import EscapeVaultMapView

app_name = "escapevault"

urlpatterns = [
    path("map/", EscapeVaultMapView.as_view(), name="evmap"),
]