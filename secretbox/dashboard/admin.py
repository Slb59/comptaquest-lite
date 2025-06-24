from django.contrib import admin

from .models import Todo


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
