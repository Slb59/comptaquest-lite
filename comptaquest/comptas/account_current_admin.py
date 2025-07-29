from django.contrib import admin

from .models import CurrentAccount


@admin.register(CurrentAccount)
class CurrentAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "bank_name", "current_balance", "state")
    list_filter = ("bank_name", "state")
    search_fields = ("name", "user__email", "user__trigram")
    readonly_fields = ("current_balance",)
    fieldsets = (
        (None, 
            {"fields": ("user", "name", "bank_name", "account_type", "description")}
        ),
        ("Pointage", 
            {"fields": ("pointed_date", "current_pointed_date", "current_pointed_balance")}
        ),
        ("Détails", 
            {"fields": ("average_interest", "ledger_analysis", "state", "closed_date")}
        ),
        ("Métadonnées", 
            {"fields": ("created_date", "created_by", "current_balance")}
        ),
    )

    def save_model(self, request, obj, form, change):
        """
        Recalcul automatique du solde à chaque sauvegarde.
        """
        super().save_model(request, obj, form, change)
        obj.recalculate_balance()
