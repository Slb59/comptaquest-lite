from django.core.exceptions import ValidationError
from django.test import TestCase

from comptaquest.comptas.models.outgoings import ExpenseOutgoings
from tests.factories.account import CurrentAccountFactory
from tests.factories.codification import (
    CategoryCodificationFactory,
    PaymentCodificationFactory,
)


class TestOutgoingsModel(TestCase):

    def setUp(self):
        self.account = CurrentAccountFactory()
        self.outgoings = ExpenseOutgoings(
            account=self.account,
            name="Test",
            category=CategoryCodificationFactory(),
            payment_method=PaymentCodificationFactory(),
        )

    def test_outgoings_creation(self):
        self.assertEqual(self.outgoings.account, self.account)
        self.assertEqual(self.outgoings.name, "Test")
        self.assertEqual(self.outgoings.outgoings_type, "Expense")
        self.assertEqual(self.outgoings.last_integrated_date, None)
        self.assertEqual(self.outgoings.periodicity, "Monthly")
        self.assertEqual(self.outgoings.start_date, None)
        self.assertEqual(self.outgoings.end_date, None)
        self.assertEqual(self.outgoings.amount, 0)
        self.assertEqual(self.outgoings.description, None)

    def test_outgoings_clean(self):
        self.outgoings.name = "Test"
        self.outgoings.last_integrated_date = "2025-01-01"
        self.outgoings.periodicity = "Monthly"
        self.outgoings.start_date = "2025-01-01"
        self.outgoings.end_date = "2025-01-01"
        self.outgoings.amount = 100
        self.outgoings.description = "Test"
        self.outgoings.full_clean()

    def test_outgoings_invalid_clean(self):
        self.outgoings.name = "Test"
        self.outgoings.last_integrated_date = "2023-01-02"
        self.outgoings.periodicity = "Monthly"
        self.outgoings.start_date = "2023-01-02"
        self.outgoings.end_date = "2023-01-01"
        self.outgoings.amount = 100
        self.outgoings.description = "Test"
        with self.assertRaises(ValidationError):
            self.outgoings.full_clean()
