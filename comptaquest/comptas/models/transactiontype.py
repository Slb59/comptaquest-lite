from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

from comptaquest.utils.models import (CategoryCodification, IncomeCodification,
                                      PaymentCodification)

from .account import CurrentAccount


class Expense(models.Model):
    """
    Represents an expense with a category and payment method.

    Attributes:
        category (ForeignKey): The category associated with the expense.
        payment_method (ForeignKey): The payment method used for the expense.
    """

    category = models.ForeignKey(
        CategoryCodification,
        on_delete=models.CASCADE,
        related_name="%(class)s_category_expenses",
    )
    payment_method = models.ForeignKey(
        PaymentCodification,
        on_delete=models.CASCADE,
        related_name="%(class)s_payment_expenses",
    )

    class Meta(TypedModelMeta):
        abstract = True


class Income(models.Model):
    """
    Represents an income with a category and income method.

    Attributes:
        income_method (ForeignKey): The method of income (e.g., salary, investment).
        category (ForeignKey): The category associated with the income.
    """

    income_method = models.ForeignKey(
        IncomeCodification,
        on_delete=models.CASCADE,
        related_name="%(class)s_payment_incomes",
    )
    category = models.ForeignKey(
        CategoryCodification,
        on_delete=models.CASCADE,
        related_name="%(class)s_category_incomes",
    )

    class Meta(TypedModelMeta):
        abstract = True


class Transfer(models.Model):
    """
    Represents a transfer transaction between two accounts.

    Attributes:
    """

    category = models.ForeignKey(
        CategoryCodification,
        on_delete=models.CASCADE,
        related_name="%(class)s_category_incomes",
    )
    link_account = models.ForeignKey(
        CurrentAccount,
        on_delete=models.CASCADE,
        related_name="%(class)s_link_account_transfers",
        blank=False,
        null=False,
    )

    link_transfer = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        related_name="%(class)s_link_transfer",
        help_text="The link transfer of this transfer node.",
        blank=True,
        null=True,
    )

    class Meta(TypedModelMeta):
        abstract = True
