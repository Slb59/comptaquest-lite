from django.test import TestCase
from django.utils.timezone import now

from comptaquest.comptas.models.outgoingstransaction import ExpenseOutgoingsTransaction
from tests.factories.account import CurrentAccountFactory
from tests.factories.codification import CategoryCodificationFactory, PaymentCodificationFactory
from tests.factories.outgoings import ExpenseOutgoingsFactory


class TestOutgoingsTransactionModel(TestCase):
    def setUp(self):
        self.account = CurrentAccountFactory()
        self.expense = ExpenseOutgoingsTransaction(
            date_transaction=now(),
            amount=100,
            account=self.account,
            category=CategoryCodificationFactory(),
            payment_method=PaymentCodificationFactory(),
            outgoings=ExpenseOutgoingsFactory(name="Test"),
        )

    def test_expense_outgoings_transaction_creation(self):
        self.assertEqual(self.expense.amount, 100)
        self.assertEqual(self.expense.outgoings.name, "Test")
