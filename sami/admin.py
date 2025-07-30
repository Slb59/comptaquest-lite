from django.contrib import admin

from sami.models import Sami


@admin.register(Sami)
class SamiAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "user",
        "total_sleep",
        "total_food",
        "total_move",
        "total_idea",
        "total_sami",
        "weight",
    )
    list_filter = ("user", "date")
    search_fields = ("user__username", "date")
    date_hierarchy = "date"
    ordering = ("-date",)

    readonly_fields = (
        "total_sleep",
        "total_food",
        "total_move",
        "total_idea",
        "total_sami",
    )

    fieldsets = (
        ("Informations générales", {"fields": ("user", "date", "weight")}),
        (
            "Sommeil",
            {
                "fields": (
                    "bedtime",
                    "wakeup",
                    "nonstop",
                    "energy",
                    "naptime",
                    "phone",
                    "reading",
                    "total_sleep",
                )
            },
        ),
        (
            "Alimentation",
            {
                "fields": (
                    "fruits",
                    "vegetables",
                    "meals",
                    "desserts",
                    "sugardrinks",
                    "nosugardrinks",
                    "total_food",
                )
            },
        ),
        (
            "Mouvement",
            {
                "fields": (
                    "homework",
                    "garden",
                    "Outsidetime",
                    "endurancesport",
                    "yogasport",
                    "total_move",
                )
            },
        ),
        (
            "Idées",
            {
                "fields": (
                    "videogames",
                    "papergames",
                    "administrative",
                    "computer",
                    "youtube",
                    "total_idea",
                )
            },
        ),
        ("Total général", {"fields": ("total_sami",)}),
        (
            "Dates de création",
            {"classes": ("collapse",), "fields": ("created_at", "updated_at")},
        ),
    )

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
