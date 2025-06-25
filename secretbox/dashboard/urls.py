from django.urls import path

from .views import TodoCreateView

app_name = "dashboard"

urlpatterns = [
    path("add/", TodoCreateView.as_view(), name="add_todo"),
]
