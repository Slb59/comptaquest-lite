from django.urls import path

from .views import DiaryEntryCreateView, DiaryEntryListView, generate_pdf

app_name = "diarylab"

urlpatterns = [
    path("add/", DiaryEntryCreateView.as_view(), name="add_entry"),
    path("list/", DiaryEntryListView.as_view(), name="list_entries"),
    path("pdf/<int:year>/<int:month>/", generate_pdf, name="generate_pdf"),
]
