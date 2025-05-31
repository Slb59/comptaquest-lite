from django.urls import path

from .views import StartPerformanceView

app_name = "performances"

urlpatterns = [
    path("", StartPerformanceView.as_view(), name="launch"),
]
