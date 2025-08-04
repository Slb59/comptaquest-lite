from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .sami_model import Sami


@admin.register(Sami)
class SamiAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "user",
        "get_total_sleep",
        "get_total_food",
        "get_total_move",
        "get_total_idea",
        "get_total_sami",
        "weight",
    )
    list_filter = ("user", "date")
    search_fields = ("user__username", "date")
    date_hierarchy = "date"
    ordering = ("-date",)

    readonly_fields = (
        "get_total_sleep",
        "get_total_food",
        "get_total_move",
        "get_total_idea",
        "get_total_sami",
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
                    "get_total_sleep",
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
                    "get_total_food",
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
                    "get_total_move",
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
                    "get_total_idea",
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

    def get_total_sleep(self, obj):
        return obj.metrics.total_sleep
    get_total_sleep.short_description = _("Total Sommeil")

    def get_total_food(self, obj):
        return obj.metrics.total_food
    get_total_food.short_description = _("Total Alimentation")

    def get_total_move(self, obj):
        return obj.metrics.total_move
    get_total_move.short_description = _("Total Mouvement")

    def get_total_idea(self, obj):
        return obj.metrics.total_idea
    get_total_idea.short_description = _("Total Idées")

    def get_total_sami(self, obj):
        return obj.metrics.total_sami
    get_total_sami.short_description = _("Total Sami")
