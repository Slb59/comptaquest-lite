from django.urls import path

app_name = "escapevault"

urlpatterns = [
    path("map/", EscapeVaultMapView.as_view(), name="evmap"),
]