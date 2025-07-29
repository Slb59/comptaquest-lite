from decimal import Decimal

from django.db import models
from django.db.models import DecimalField, F, Sum
from django.utils.translation import gettext_lazy as _

from .account_abstract_model import AbstractAccount


class InvestmentAccount(AbstractAccount):

    account_type = models.CharField(
        max_length=15,
        default="Investment",
        editable=False,  # Fixed account type
    )

    def calculate_portfolio_value(self) -> Decimal:
        """
        Calcule la somme totale du portefeuille basé sur les actifs liés.
        """
        total = self.assets.aggregate(
            total_value=Sum(
                F("quantity") * F("price"), 
                output_field=DecimalField(max_digits=16, decimal_places=4)
            )
        )["total_value"] or Decimal("0.0")
        return total

    def recalculate_balance(self):
        """
        Redéfinit le solde actuel en fonction de la valeur du portefeuille.
        """
        self.current_balance = self.calculate_portfolio_value()
        self.save(update_fields=["current_balance"])


class InvestmentAsset(models.Model):
    account = models.ForeignKey("InvestmentAccount", on_delete=models.CASCADE, related_name="assets")

    designation = models.CharField(max_length=100, verbose_name=_("Designation"))

    asset_type = models.CharField(
        max_length=30,
        choices=[
            ("Stock", _("Stock")),
            ("Bond", _("Bond")),
            ("ETF", _("ETF")),
            ("Crypto", _("Crypto")),
            ("Other", _("Other")),
        ],
        default="Stock",
        verbose_name=_("Type"),
    )

    quantity = models.DecimalField(
        max_digits=12, 
        decimal_places=4, 
        default=0, 
        verbose_name=_("Quantité")
    )

    price = models.DecimalField(
        max_digits=12, 
        decimal_places=4, 
        default=0, 
        verbose_name=_("Cours ")
    )

    def get_valuation(self) -> Decimal:
        """
        Returns the valuation of the asset = quantity x price.
        """
        return self.quantity * self.price

    def __str__(self):
        return f"{self.designation} ({self.asset_type}) - {self.quantity} * {self.price}"
