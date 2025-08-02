from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from .choices import ACCOUNT_CHOICES, BANK_CHOICES, STATE_CHOICES

from django.contrib.auth import get_user_model

Member = get_user_model()

class AbstractAccount(models.Model):

    user = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="%(class)s_user_accounts",
        db_index=True,
    )

    name = models.CharField(max_length=50)

    account_type = models.CharField(
        max_length=15,
        choices=ACCOUNT_CHOICES,
        default="Current",
    )

    # The last pointed date
    pointed_date = models.DateField(blank=True, null=True)

    # The account is to be pointed at this date, but not finished
    current_pointed_date = models.DateField(
        blank=True,
        null=True,
    )
    # The amount of the balance that is being to be pointed
    current_pointed_balance = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
    )
    # The last amount of balance pointed
    current_balance = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
    )

    average_interest = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        help_text=_("The average interest that is expected for"),
    )

    ledger_analysis = models.BooleanField(
        default=True, help_text=_("If the account is include in the ledger analysis")
    )

    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        db_index=True,
    )

    state = models.CharField(max_length=15, choices=STATE_CHOICES, default="Open")
    closed_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "After the closed date it is not possibile to add transaction or modify this account"
        ),
    )

    bank_name = models.CharField(max_length=15, choices=BANK_CHOICES, default="CA")
    description = models.TextField(blank=True, null=True)

    class Meta(TypedModelMeta):
        abstract = True

    def __str__(self):
        """
        Returns a string representation of the account, including the user's trigram and account name.
        """
        return f"{self.user.trigram} - {self.name} - {self.bank_name}"

    def get_transaction_sum(self, transaction_type, **filters):
        """
        Calculate the sum of transactions of a given type with additional filters.

        Args:
            transaction_type (str): The type of transaction (e.g., 'Expense', 'Income', etc.).
            **filters: Additional filters for querying the transactions.

        Returns:
            Decimal: The sum of the transaction amounts or 0 if no matching transactions exist.
        """
        related_name_map = {
            "Expense": "expensetransaction_account_transactions",
            "Income": "incometransaction_account_transactions",
            "Transfer": "transfertransaction_account_transactions",
        }

        related_name = related_name_map.get(transaction_type)
        if not related_name:
            raise ValueError(f"Unknown transaction type: {transaction_type}")

        # Use the dynamically determined related name
        return (
            getattr(self, related_name)
            .filter(**filters)
            .aggregate(Sum("amount"))["amount__sum"]
            or 0
        )

    def recalculate_balance(self):
        """
        Recalculate the current balance based on all related transactions.
        """
        total_income = self.get_transaction_sum(transaction_type="Income")
        total_expense = self.get_transaction_sum(transaction_type="Expense")

        total_transfer = self.get_transaction_sum(transaction_type="Transfer")
        self.current_balance = total_income - total_expense + total_transfer
        self.save(update_fields=["current_balance"])
