from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _

from .account import CurrentAccount
from .ledger import Ledger
from .transactiontype import Expense, Income, Transfer


class TransactionManager(models.Manager):
    """
    Custom manager for the Transaction model to provide additional query capabilities.

    Methods:
        expenses: Returns all transactions of type 'Expense'.
        income: Returns all transactions of type 'Income'.
        transfers: Returns all transactions of type 'Transfer'.
        by_date_range: Returns transactions within a specified date range.
    """

    def expenses(self):
        """
        Returns all transactions of type 'Expense'.

        Returns:
            QuerySet: Transactions filtered by type 'Expense'.
        """
        return self.filter(transaction_type="Expense")

    def income(self):
        """
        Returns all transactions of type 'Income'.

        Returns:
            QuerySet: Transactions filtered by type 'Income'.
        """
        return self.filter(transaction_type="Income")

    def transfers(self):
        """
        Returns all transactions of type 'Transfer'.

        Returns:
            QuerySet: Transactions filtered by type 'Transfer'.
        """
        return self.filter(transaction_type="Transfer")

    def by_date_range(self, start_date, end_date):
        """
        Returns transactions within the specified date range.

        Args:
            start_date (datetime): The start of the date range.
            end_date (datetime): The end of the date range.

        Returns:
            QuerySet: Transactions within the given date range.
        """
        return self.filter(date_transaction__range=(start_date, end_date))


class Transaction(models.Model):
    """
    Represents a financial transaction associated with an account and ledger.

    Attributes:
        account (ForeignKey): The account associated with the transaction.
        ledger (ForeignKey): The ledger associated with the transaction.
        date_transaction (DateTimeField): The date the transaction occurred.
        amount (DecimalField): The amount of the transaction.
        date_pointed (DateTimeField): The date the transaction was reconciled or pointed.
        description (TextField): A brief description or details about the transaction.
        updatable (BooleanField): Indicates whether the transaction can be updated.
        transaction_type (CharField): Specifies the type of transaction (Expense, Income, Transfer, Outgoings).

    Usage:
        # Normal transaction
        transaction = ExpenseTransaction.objects.get(id=1)
        try:
            transaction.delete()  # Will mark as deleted if not pointed
        except ProtectedError:
            print("Cannot delete - transaction is pointed")

        # Transfer transaction
        transfer = TransferTransaction.objects.get(id=1)
        try:
            transfer.delete()  # Will mark both sides as deleted if neither is pointed
        except ProtectedError:
            print("Cannot delete - one or both transactions are pointed")

        # To query only active transactions
        active_transactions = ExpenseTransaction.objects.filter(status=Transaction.TransactionStatus.ACTIVE)
    """

    class TransactionType(models.TextChoices):
        EXPENSE = "Expense", "expense"
        INCOME = "Income", "income"
        TRANSFER = "Transfer", "transfer"
        OUTGOINGS = "Outgoings", "outgoings"

    class TransactionStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        DELETED = "deleted", "Deleted"

    account = models.ForeignKey(
        CurrentAccount,
        on_delete=models.CASCADE,
        related_name="%(class)s_account_transactions",
        db_index=True,  # Index for faster queries related to account
        null=False,
    )

    ledger = models.ForeignKey(
        Ledger,
        on_delete=models.CASCADE,
        related_name="%(class)s_ledger_transactions",
        db_index=True,  # Index for ledger-related queries
        null=True,
        blank=True,
    )

    date_transaction = models.DateTimeField(
        blank=False,
        null=False,
        db_index=True,  # Index for filtering or ordering by date
    )
    amount = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    date_pointed = models.DateTimeField(blank=True, null=True, db_index=True)
    description = models.TextField(
        validators=[MaxLengthValidator(500)], blank=True, null=True
    )
    updatable = models.BooleanField(default=True)
    transaction_type = models.CharField(
        max_length=15,
        choices=TransactionType.choices,
        default=TransactionType.EXPENSE,
        db_index=True,  # Index for filtering by transaction type
    )

    status = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.ACTIVE,
        db_index=True,
    )

    objects = TransactionManager()  # Attach the custom manager

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.account.name}-{self.date_transaction}-{self.amount}"

    def soft_delete(self):
        """
        Marks the transaction as deleted if conditions allow.
        Raises ProtectedError if the transaction cannot be deleted.
        """
        if self.date_pointed:
            raise ProtectedError(
                _("Cannot delete transaction that has been pointed/reconciled"), self
            )

        self.status = self.TransactionStatus.DELETED
        self.save(update_fields=["status"])

    def delete(self, *args, **kwargs):
        """
        Override delete method to implement soft delete behavior.
        """
        try:
            self.soft_delete()
        except ProtectedError as e:
            raise e


class ExpenseTransaction(Transaction, Expense):
    """
    Represents a financial transaction specifically categorized as an expense.
    """

    class Meta(Transaction.Meta):
        indexes = [
            # Compound index for account and transaction type
            models.Index(
                fields=["account", "transaction_type"], name="idx_expense_account_type"
            ),
            # Compound index for date and account
            models.Index(
                fields=["date_transaction", "account"], name="idx_expense_date_account"
            ),
            models.Index(fields=["status"], name="idx_expense_status"),
        ]


class IncomeTransaction(Transaction, Income):
    """
    Represents a financial transaction specifically categorized as income.
    """

    class Meta(Transaction.Meta):
        indexes = [
            # Compound index for account and transaction type
            models.Index(
                fields=["account", "transaction_type"], name="idx_income_account_type"
            ),
            # Compound index for date and account
            models.Index(
                fields=["date_transaction", "account"], name="idx_income_date_account"
            ),
            models.Index(fields=["status"], name="idx_income_status"),
        ]


class TransferTransaction(Transaction, Transfer):
    """
    Represents a financial transaction specifically categorized as a transfer.
    """

    ...
    # contra_entry?

    class Meta(Transaction.Meta):
        indexes = [
            # Compound index for account and transaction type
            models.Index(
                fields=["account", "transaction_type"], name="idx_transfer_account_type"
            ),
            # Compound index for date and account
            models.Index(
                fields=["date_transaction", "account"], name="idx_transfer_date_account"
            ),
            models.Index(fields=["status"], name="idx_transfer_status"),
        ]

    def __str__(self):
        return f"Transfer {self.date_transaction}-{self.amount}: {self.account}->{self.link_account}"

    def save(self, *args, **kwargs):
        # Check if this is a new transaction without a link
        creating_new = not self.pk and not self.link_transfer

        # First save the current transaction
        super().save(*args, **kwargs)

        # If this is a new transaction without a link, create the reverse transaction
        if creating_new:
            reverse_transaction = TransferTransaction.objects.create(
                date_transaction=self.date_transaction,
                amount=-self.amount,
                account=self.link_account,
                link_account=self.account,
                link_transfer=self,
                category=self.category,
            )

            # Update the current transaction with the link
            self.link_transfer = reverse_transaction
            self.save(update_fields=["link_transfer"])

    def soft_delete(self):
        """
        Extends soft delete to handle reciprocal transaction.
        Both transactions must be eligible for deletion.
        """
        # First check if either transaction is pointed
        if self.date_pointed or (
            self.link_transfer and self.link_transfer.date_pointed
        ):
            raise ProtectedError(
                _(
                    "Cannot delete transfer - one or both transactions have been pointed/reconciled"
                ),
                self,
            )

        # If we get here, neither transaction is pointed, so we can proceed
        self.status = self.TransactionStatus.DELETED
        self.save(update_fields=["status"])

        # Also mark the linked transaction as deleted if it exists
        if self.link_transfer:
            self.link_transfer.status = self.TransactionStatus.DELETED
            self.link_transfer.save(update_fields=["status"])
