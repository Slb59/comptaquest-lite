import pytest
from django.test import TestCase

from tests.factories.account import CurrentAccountFactory
from tests.factories.transaction import ExpenseTransactionFactory, IncomeTransactionFactory


@pytest.mark.django_db
class TestAccountModel(TestCase):
    def setUp(self):
        self.account = CurrentAccountFactory(name="Test Account", current_balance=0)

    def test_account_name(self):
        self.assertEqual(self.account.name, "Test Account")

    def test_account_type(self):
        self.assertEqual(self.account.account_type, "Current")

    def test_account_pointed_date(self):
        self.assertIsNone(self.account.pointed_date)

    def test_account_current_pointed_date(self):
        self.assertIsNone(self.account.current_pointed_date)

    def test_account_current_pointed_balance(self):
        self.assertEqual(self.account.current_pointed_balance, 0)

    def test_account_current_balance(self):
        self.assertEqual(self.account.current_balance, 0)

    def test_account_average_interest(self):
        self.assertEqual(self.account.average_interest, 0)

    def test_account_created_date(self):
        self.assertIsNone(self.account.created_date)

    def test_account_closed_date(self):
        self.assertIsNone(self.account.closed_date)

    def test_account_bank_name(self):
        self.assertEqual(self.account.bank_name, "CA")

    def test_account_str(self):
        self.assertEqual(str(self.account), "MB1 - Test Account")


@pytest.mark.django_db
class TestAccountFunctionsModel(TestCase):
    def setUp(self):
        self.account = CurrentAccountFactory()
        self.expense = ExpenseTransactionFactory(account=self.account, amount=100)
        self.income = IncomeTransactionFactory(account=self.account, amount=80)

    def test_get_transaction_sum_expense(self):
        total = self.account.get_transaction_sum("Expense")
        self.assertEqual(total, 100.0)

    def test_get_transaction_sum_income(self):
        total = self.account.get_transaction_sum("Income")
        self.assertEqual(total, 80.0)

    def test_account_recalculate_balance(self):
        self.account.current_balance = 100
        self.account.save()
        self.account.recalculate_balance()
        self.assertEqual(self.account.current_balance, -20)
