from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import ColorParameter, Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("description", "user", "state", "planned_date", "priority")
    list_filter = ("state", "category", "who", "place", "priority")
    search_fields = ("description", "user__trigram", "note")
    date_hierarchy = "planned_date"
    ordering = ("-planned_date",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "description",
                    "state",
                    "duration",
                    "appointment",
                    "category",
                    "who",
                    "place",
                    "periodic",
                    "report_date",
                    "planned_date",
                    "priority",
                    "done_date",
                    "note",
                )
            },
        ),
    )


@admin.register(ColorParameter)
class ColorParameterAdmin(admin.ModelAdmin):
    list_display = (
        "priority",
        "periodic",
        "category",
        "place",
        "color_display",
    )

    list_filter = (
        "priority",
        "periodic",
        "category",
        "place",
    )
    search_fields = ("color",)

    def color_display(self, obj):
        return format_html(
            '<div style="width: 60px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>', obj.color
        )

    color_display.short_description = _("Couleur")
