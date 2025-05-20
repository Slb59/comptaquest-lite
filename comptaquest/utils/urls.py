from django.urls import path

from .views import CategoryListView, SettingsView

app_name = "utils"

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("settings/", SettingsView.as_view(), name="settings"),
]
