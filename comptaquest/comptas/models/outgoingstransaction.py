from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .outgoings import ExpenseOutgoings, IncomeOutgoings, TransferOutgoings
from .transaction import ExpenseTransaction, IncomeTransaction, TransferTransaction


class OutgoingsTransaction(models.Model):
    """
    Represents a transaction associated with recurring outgoings.

    Attributes:
        last_transaction (ForeignKey): A reference to the last transaction in the outgoing sequence.
        previous_transaction (ForeignKey): A reference to the previous transaction in the outgoing sequence.
        outgoings_transaction_type (CharField): Specifies the type of the outgoing transaction (Expense, Income, or Transfer).
    """

    class OutgoingsTransactionType(models.TextChoices):
        EXPENSE = "Expense", "expense"
        INCOME = "Income", "income"
        TRANSFER = "Transfer", "transfer"

    last_transaction = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="%(class)s_last_transactions",
        blank=True,
        null=True,
    )
    previous_transaction = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="%(class)s_previous_transactions",
        blank=True,
        null=True,
    )

    def clean(self):
        """
        Validates the integrity of the OutgoingsTransaction instance.

        Ensures that:
        - `last_transaction` and `previous_transaction` do not reference the same object as `self`.
        - Circular references are prevented in the `last_transaction` and `previous_transaction` chains.

        Raises:
            ValidationError: If any validation check fails.
        """
        super().clean()

        # Ensure last_transaction and previous_transaction are not the same as self
        if self.last_transaction == self:
            raise ValidationError("last_transaction cannot reference the same object.")
        if self.previous_transaction == self:
            raise ValidationError(
                "previous_transaction cannot reference the same object."
            )

        # Prevent circular references in last_transaction
        if self.is_circular_reference(self.last_transaction):
            raise ValidationError("Circular reference detected in last_transaction.")

        # Prevent circular references in previous_transaction
        if self.is_circular_reference(self.previous_transaction):
            raise ValidationError(
                "Circular reference detected in previous_transaction."
            )

    def is_circular_reference(self, transaction):
        """
        Check if the given transaction indirectly references `self`, creating a circular reference.

        Args:
            transaction (OutgoingsTransaction): The transaction to validate.

        Returns:
            bool: True if a circular reference is detected, False otherwise.
        """
        visited = set()
        current = transaction
        while current:
            if current == self:
                return True
            if current in visited:
                break  # Prevent infinite loops in case of corrupt data
            visited.add(current)
            current = current.last_transaction  # Traverse the chain
        return False

    class Meta:
        abstract = True
        # constraints = [
        #     models.CheckConstraint(
        #         check=~models.Q(last_transaction=models.F("id")),
        #         name="check_no_self_reference_last_transaction",
        #     ),
        #     models.CheckConstraint(
        #         check=~models.Q(previous_transaction=models.F("id")),
        #         name="check_no_self_reference_previous_transaction",
        #     ),
        # ]


class ExpenseOutgoingsTransaction(OutgoingsTransaction, ExpenseTransaction):
    """
    Represents an expense transaction associated with recurring outgoings.
    """

    outgoings = models.ForeignKey(
        ExpenseOutgoings,
        verbose_name=_("Outgoings Expense"),
        on_delete=models.CASCADE,
        related_name="%(class)s_outgoings_transactions",
    )


class IncomeOutgoingsTransaction(OutgoingsTransaction, IncomeTransaction):
    """
    Represents an income transaction associated with recurring outgoings.
    """

    outgoings = models.ForeignKey(
        IncomeOutgoings,
        verbose_name=_("Outgoings Income"),
        on_delete=models.CASCADE,
        related_name="%(class)s_outgoings_transactions",
    )


class TransferOutgoingsTransaction(OutgoingsTransaction, TransferTransaction):
    """
    Represents a transfer transaction associated with recurring outgoings.
    """

    outgoings = models.ForeignKey(
        TransferOutgoings,
        verbose_name=_("Outgoings Transfer"),
        on_delete=models.CASCADE,
        related_name="%(class)s_outgoings_transactions",
    )
