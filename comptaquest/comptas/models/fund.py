from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .account import InvestmentAccount


class FundDistribution(models.Model):
    """
    Represents the distribution of funds within an investment account.

    Attributes:
        fund_name (CharField): The name of the fund.
        prct (IntegerField): The percentage of the fund allocation (0-100).
        fund_type (CharField): The type of fund.
        investment_account (ForeignKey): The associated investment account.
    """

    fund_name = models.CharField(max_length=50)
    prct = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fund_type = models.CharField(max_length=50)
    investment_account = models.ForeignKey(
        InvestmentAccount,
        on_delete=models.CASCADE,
        related_name="%(class)s_fund_distribution_accounts",
        db_index=True,
    )


class FundHistory(models.Model):
    """
    Represents the historical data of a fund within an investment account.

    Attributes:
        date_value (DateTimeField): The date of the historical record.
        amount (DecimalField): The value of the fund at the recorded date.
        notes (CharField): Additional notes about the record.
        investment_account (ForeignKey): The associated investment account.
    """

    date_value = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    notes = models.CharField(max_length=300, blank=True)
    investment_account = models.ForeignKey(
        InvestmentAccount,
        on_delete=models.CASCADE,
        related_name="%(class)s_fund_distribution_accounts",
        db_index=True,
    )
