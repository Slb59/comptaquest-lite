# urls.py
from django.urls import path
from .views import DashboardView, update_duration

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('update-duration/<int:todo_id>/', update_duration, name='update_duration'),
]
