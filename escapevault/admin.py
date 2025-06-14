import csv
from io import StringIO

from django.contrib import admin
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django_countries.fields import CountryField

from .models import NomadePosition


@admin.register(NomadePosition)
class NomadePositionAdmin(admin.ModelAdmin):
    # Configuration générale
    list_display = ("name", "city", "country", "stars", "opening_date")
    list_filter = ("city", "country", "category", "stars", "opening_date")
    search_fields = ("name", "address", "category")

    # Organisation des champs dans l'interface
    fieldsets = [
        ("Informations principales", {"fields": ["name", "address"]}),
        ("Localisation", {"fields": ["city", "country", "latitude", "longitude"]}),
        ("Évaluation", {"fields": ["stars", "reviews"]}),
        ("Dates et catégorie", {"fields": ["opening_date", "closing_date", "category"]}),
    ]

    # Actions personnalisées
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        f = StringIO()
        writer = csv.writer(f)

        # En-tête du CSV
        header = [
            "Nom",
            "Adresse",
            "Ville",
            "Pays",
            "Latitude",
            "Longitude",
            "Étoiles",
            "Catégorie",
            "Date d'ouverture",
            "Date de fermeture",
        ]

        writer.writerow(header)

        # Données
        for obj in queryset:
            writer.writerow(
                [
                    smart_str(obj.name),
                    smart_str(obj.address),
                    smart_str(obj.city),
                    smart_str(obj.country.name),
                    smart_str(obj.latitude),
                    smart_str(obj.longitude),
                    smart_str(obj.stars),
                    smart_str(obj.category),
                    smart_str(obj.opening_date),
                    smart_str(obj.closing_date),
                ]
            )

        f.seek(0)
        response = HttpResponse(f.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=positions_nomades.csv"
        return response

    export_to_csv.short_description = "Exporter sélection au CSV"

    # Personnalisation des vues
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            return queryset.filter(city__isnull=False)
        return queryset

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.id = uuid.uuid4()
        super().save_model(request, obj, form, change)
