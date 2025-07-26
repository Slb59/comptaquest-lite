from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django_stubs_ext.db.models import TypedModelMeta

from comptaquest.comptas.models.transaction import (ExpenseTransaction,
                                                    IncomeTransaction)
from secretbox.users.models import Member


class HealthManager(models.Manager):
    def total_expenses_by_user(self, user, year=None):
        """
        Calculate total health expenses for a user, optionally filtered by year.

        Args:
            user (Member): User to calculate expenses for
            year (int, optional): Specific year to calculate expenses. Defaults to current year.

        Returns:
            Decimal: Total health expenses

        usage:
            # Get total expenses for current year
            total_this_year = Health.objects.total_expenses_by_user(user)

            # Get total expenses for a specific year
            total_2024 = Health.objects.total_expenses_by_user(user, 2024)
        """
        if year is None:
            year = timezone.now().year

        return self.filter(user=user, date__year=year).aggregate(total_expenses=Sum("amount"))["total_expenses"] or 0


class Secu(models.Model):
    """
    Represents social security income transaction details.

    Attributes:
        theoritical_date (DateField): Date of theoretical social security transaction.
        amount (DecimalField): Total amount of social security transaction.
        withheld_amount (DecimalField): Amount withheld from the transaction.
        income_transaction (ForeignKey): Related income transaction.
    """

    theoritical_date = models.DateField(default=timezone.now, db_index=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    withheld_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    income_transaction = models.ForeignKey(
        IncomeTransaction,
        on_delete=models.CASCADE,
        related_name="secu_income_transactions",
    )


class Mutuelle(models.Model):
    """
    Represents supplementary health insurance income transaction details.

    Attributes:
        theorical_date (DateField): Date of theoretical mutuelle transaction.
        amount (DecimalField): Total amount of mutuelle transaction.
        income_transaction (ForeignKey): Related income transaction.
    """

    theorical_date = models.DateField(default=timezone.now, db_index=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    income_transaction = models.ForeignKey(
        IncomeTransaction,
        on_delete=models.CASCADE,
        related_name="mutuelle_income_transactions",
    )


class Health(models.Model):
    """
    Tracks individual health-related expenses.

    Attributes:
        date (DateField): Date of health expense.
        amount (DecimalField): Total expense amount.
        expense_transaction (ForeignKey): Related expense transaction.
        subject (CharField): Brief subject of the health expense.
        description (TextField): Detailed description of the health expense.
        created_at (DateTimeField): Timestamp of record creation.
        updated_at (DateTimeField): Timestamp of last record update.
        user (ForeignKey): User associated with the health expense.
        secu (OneToOneField): Related social security transaction.
        mutuelle (OneToOneField): Related supplementary health insurance transaction.
    """

    objects = HealthManager()
    date = models.DateField(default=timezone.now, db_index=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    expense_transaction = models.ForeignKey(
        ExpenseTransaction,
        on_delete=models.CASCADE,
        related_name="health_expense_transactions",
    )
    subject = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="user_healths")
    secu = models.OneToOneField(Secu, on_delete=models.CASCADE, related_name="secu")
    mutuelle = models.OneToOneField(Mutuelle, on_delete=models.CASCADE, related_name="mutuelle")

    class Meta(TypedModelMeta):
        verbose_name = "health"
        verbose_name_plural = "healths"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "date"]),
        ]

    def __str__(self):
        """
        String representation of the Health model.

        Returns:
            str: Formatted string with user trigram, subject, and date.
        """
        return f"{self.user.trigram} - {self.subject} - {self.date}"

    @property
    def reimbursement_total(self):
        """Calculate total reimbursements."""
        return self.secu.income_transaction.amount + self.mutuelle.income_transaction.amount

    @property
    def remains_amount(self):
        """
        Calculate the remaining amount after social security and mutuelle reimbursements.

        Returns:
            Decimal: Remaining expense amount after reimbursements.
        """
        return self.amount - self.reimbursement_total

    def clean(self):
        """Validate that reimbursements do not exceed total amount."""
        if self.reimbursement_total > self.amount:
            raise ValidationError("Reimbursements cannot exceed total expense amount.")
