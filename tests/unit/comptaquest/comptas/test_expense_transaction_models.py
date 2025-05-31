from django.test import TestCase
from django.utils.timezone import now

from comptaquest.comptas.models.transaction import ExpenseTransaction
from tests.factories.account import CurrentAccountFactory
from tests.factories.codification import (CategoryCodificationFactory,
                                          PaymentCodificationFactory)


class TestExpenseTransactionModel(TestCase):

    def setUp(self):
        self.account = CurrentAccountFactory()
        self.expense = ExpenseTransaction(
            date_transaction=now(),
            amount=100,
            account=self.account,
            category=CategoryCodificationFactory(),
            payment_method=PaymentCodificationFactory(),
        )

    def test_expense_transaction_creation(self):
        self.assertEqual(self.expense.amount, 100)
