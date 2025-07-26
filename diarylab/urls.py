from django.urls import path

from .views import DiaryDeleteView, DiaryEditView, DiaryEntryCreateView, DiaryEntryListView, generate_pdf

app_name = "diarylab"

urlpatterns = [
    path("add/", DiaryEntryCreateView.as_view(), name="add_entry"),
    path("list/", DiaryEntryListView.as_view(), name="list_entries"),
    path("<int:pk>/edit/", DiaryEditView.as_view(), name="edit_entry"),
    path("<int:pk>/delete/", DiaryDeleteView.as_view(), name="delete_entry"),
    path("pdf/<int:year>/<int:month>/", generate_pdf, name="generate_pdf"),
]
