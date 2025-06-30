from django.urls import path

from .views import TodoCreateView, TodoDeleteView, TodoUpdateView

app_name = "dashboard"

urlpatterns = [
    path("add/", TodoCreateView.as_view(), name="add_todo"),
    path("edit/<int:pk>/", TodoUpdateView.as_view(), name="edit_todo"),
    path("delete/<int:pk>/", TodoDeleteView.as_view(), name="delete_todo"),
]
