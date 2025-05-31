from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class AbstractAccount(models.Model):

    class AccountType(models.TextChoices):
        CURRENT = "Current", "current"
        INVESTMENT = "Investment", "investment"

    class Bank(models.TextChoices):
        CE = "CE", "CE"
        CA = "CA", "CA"
        GMF = "GMF", "GMF"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_user_accounts",
        db_index=True,
    )
    name = models.CharField(max_length=50, help_text=_("the account name"))
    account_type = models.CharField(
        max_length=15,
        choices=AccountType.choices,
        default=AccountType.CURRENT,
        help_text=_("Account could be a current account or an investment account"),
    )
    pointed_date = models.DateTimeField(blank=True, null=True, help_text=_("The last pointed date"))
    current_pointed_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("The account is to be pointed at this date, but not finished"),
    )
    current_pointed_balance = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        help_text=_("The amount of the balance that is being to be pointed"),
    )
    current_balance = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        help_text=_("The last amount of balance pointed"),
    )

    average_interest = models.DecimalField(
        default=0,
        max_digits=8,
        decimal_places=2,
        help_text=_("The average interest that is expected for"),
    )

    ledger_analysis = models.BooleanField(default=True, help_text=_("If the account is include in the ledger analysis"))

    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        db_index=True,
    )
    closed_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("After the closed date it is not possibile to add transaction or modify this account"),
    )

    bank_name = models.CharField(max_length=15, choices=Bank.choices, default=Bank.CA)
    description = models.TextField(blank=True, null=True)

    class Meta(TypedModelMeta):
        abstract = True

    def __str__(self):
        """
        Returns a string representation of the account, including the user's trigram and account name.
        """
        return f"{self.user.trigram} - {self.name}"

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
        return getattr(self, related_name).filter(**filters).aggregate(Sum("amount"))["amount__sum"] or 0

    def recalculate_balance(self):
        """
        Recalculate the current balance based on all related transactions.
        """
        total_income = self.get_transaction_sum(transaction_type="Income")
        total_expense = self.get_transaction_sum(transaction_type="Expense")

        total_transfer = self.get_transaction_sum(transaction_type="Transfer")
        self.current_balance = total_income - total_expense + total_transfer
        self.save(update_fields=["current_balance"])


class CurrentAccount(AbstractAccount):
    account_type = models.CharField(
        max_length=15,
        default="Current",
        editable=False,  # Fixed account type
    )


class InvestmentAccount(AbstractAccount):

    account_type = models.CharField(
        max_length=15,
        default="Investment",
        editable=False,  # Fixed account type
    )
