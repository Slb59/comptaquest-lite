from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models

from .account import CurrentAccount
from .transactiontype import Expense, Income, Transfer


class Outgoings(models.Model):
    """
    Represents a recurring outgoing transaction associated with an account.

    Attributes:
        account (ForeignKey): The account associated with the outgoing.
        name (CharField): The name or description of the outgoing.
        outgoingstype (CharField): The type of outgoing (Expense, Income, Transfer).
        last_integrated_date (DateTimeField): The date of the last integration.
        periodicity (CharField): The periodicity of the outgoing (e.g., Monthly, Quarterly).
        start_date (DateTimeField): The start date for the outgoing.
        end_date (DateTimeField): The end date for the outgoing (if applicable).
        amount (DecimalField): The amount of the outgoing.
        description (TextField): Additional information about the outgoing.
    """

    class Periodicity(models.TextChoices):
        MONTHLY = "Monthly", "monthly"
        HALFYEARLY = "Half-yearly", "half-yearly"
        QUARTERLY = "Quaterly", "quaterly"
        YEARLY = "Yearly", "yearly"

    class OutgoingsType(models.TextChoices):
        EXPENSE = "Expense", "expense"
        INCOME = "Income", "income"
        TRANSFER = "Transfer", "transfer"

    account = models.ForeignKey(
        CurrentAccount,
        on_delete=models.CASCADE,
        related_name="%(class)s_account_outgoings",
        db_index=True,
    )
    name = models.CharField(max_length=50, blank=False, null=False)
    outgoings_type = models.CharField(
        max_length=15, choices=OutgoingsType.choices, default=OutgoingsType.EXPENSE
    )
    last_integrated_date = models.DateTimeField(blank=True, null=True)
    periodicity = models.CharField(
        max_length=15, choices=Periodicity.choices, default=Periodicity.MONTHLY
    )
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    description = models.TextField(
        validators=[MaxLengthValidator(500)], blank=True, null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        db_index=True,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("start_date cannot be later than end_date.")


class ExpenseOutgoings(Outgoings, Expense):
    """
    Represents an outgoing expense transaction associated with an account.
    """

    outgoings_type = models.CharField(
        max_length=15,
        default="Expense",
        editable=False,  # Fixed account type
    )


class IncomeOutgoings(Outgoings, Income):
    """
    Represents an outgoing income transaction associated with an account.
    """

    outgoings_type = models.CharField(
        max_length=15,
        default="Income",
        editable=False,  # Fixed account type
    )


class TransferOutgoings(Outgoings, Transfer):
    """
    Represents an outgoing transfer transaction associated with an account.
    """

    outgoings_type = models.CharField(
        max_length=15,
        default="Transfer",
        editable=False,  # Fixed account type
    )
