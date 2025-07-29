from django.contrib import admin

from .account_investment_model import InvestmentAccount, InvestmentAsset


class InvestmentAssetInline(admin.TabularInline):
    model = InvestmentAsset
    extra = 1  # Nombre de lignes vides proposées par défaut
    fields = ("designation", "asset_type", "quantity", "price", "get_valuation")
    readonly_fields = ("get_valuation",)

    def get_valuation(self, obj):
        return obj.get_valuation()

    get_valuation.short_description = "Valorisation"


@admin.register(InvestmentAccount)
class InvestmentAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "bank_name", "current_balance")
    inlines = [InvestmentAssetInline]
    readonly_fields = ("current_balance",)

    def save_model(self, request, obj, form, change):
        """
        Sauvegarde le compte et met à jour le solde automatiquement.
        """
        super().save_model(request, obj, form, change)
        obj.recalculate_balance()

    def save_related(self, request, form, formsets, change):
        """
        Sauvegarde les objets liés (assets) et met à jour le solde après.
        """
        super().save_related(request, form, formsets, change)
        form.instance.recalculate_balance()
