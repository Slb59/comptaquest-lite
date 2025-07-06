from django.urls import path

from .views import TodoCreateView, TodoDeleteView, TodoUpdateView, check_todo_state, todo_mark_done

app_name = "dashboard"

urlpatterns = [
    path("add/", TodoCreateView.as_view(), name="add_todo"),
    path("edit/<int:pk>/", TodoUpdateView.as_view(), name="edit_todo"),
    path("delete/<int:pk>/", TodoDeleteView.as_view(), name="delete_todo"),
    path("todo/<int:pk>/check_state/", check_todo_state, name="check_todo_state"),

    path("todo/<int:pk>/done/", todo_mark_done, name="mark_done"),
]

