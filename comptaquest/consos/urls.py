from django.urls import path

from .views import (ConsosEdfCreateView, ConsosEdfDetailView, ConsosEdfView,
                    ConsosWaterCreateView, ConsosWaterDetailView,
                    ConsosWaterView)

app_name = "consos"


urlpatterns = [
    # consos water urls
    path("consoswater/", ConsosWaterView.as_view(), name="consos_water"),
    path(
        "consoswater/create/",
        ConsosWaterCreateView.as_view(),
        name="consos_water_create",
    ),
    path(
        "consoswater/<int:account_id>/",
        ConsosWaterDetailView.as_view(),
        name="consos_water_detail",
    ),
    # consos edf urls
    path("consosedf/", ConsosEdfView.as_view(), name="consos_edf"),
    path("consosedf/create/", ConsosEdfCreateView.as_view(), name="consos_edf_create"),
    path(
        "consosedf/<int:account_id>/",
        ConsosEdfDetailView.as_view(),
        name="consos_edf_detail",
    ),
]
