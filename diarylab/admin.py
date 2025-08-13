# admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    """
    Configuration of the admin interface for the DiaryEntry model.
    This class defines the display and functionality in the Django admin interface.
    """

    # List of fields displayed in the main view
    list_display = (
        "date",
        "user",
        "preview_content",
    )

    # Fields used for filtering
    list_filter = (
        "date",
        "user",
    )

    # Fields used for search
    search_fields = (
        "content",
        "user__username",
        "user__email",
    )

    # Organization of fields in the editing interface
    fieldsets = (
        (_("Main Information"), {"fields": ("date", "content", "user")}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at")}),
    )

    # Read-only fields
    readonly_fields = ("created_at", "updated_at")

    # Content preview (limited to 200 characters)
    def preview_content(self, obj):
        """Displays a preview of the diary entry content."""
        return f"{obj.content[:200]}{'...' if len(obj.content) > 200 else ''}"

    preview_content.short_description = _("Content Preview")

    # Bulk action configuration
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        """Exports the selected entries in CSV format."""
        import csv
        from io import StringIO

        from django.http import HttpResponse

        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["Date", "User", "Content", "Created at", "Updated at"])

        # Data
        for entry in queryset:
            writer.writerow(
                [
                    entry.date,
                    entry.user.username,
                    entry.content,
                    entry.created_at,
                    entry.updated_at,
                ]
            )

        response = HttpResponse(
            output.getvalue(),
            content_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=diary_entries.csv"},
        )
        return response

    export_to_csv.short_description = _("Export selection to CSV")
