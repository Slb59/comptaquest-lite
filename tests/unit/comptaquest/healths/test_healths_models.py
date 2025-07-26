from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from comptaquest.healths.models import Health, Mutuelle, Secu
from tests.factories.account import CurrentAccountFactory
from tests.factories.member import MemberFactory
from tests.factories.transaction import ExpenseTransactionFactory, IncomeTransactionFactory


class TestHealthModel(TestCase):
    def setUp(self):
        self.user = MemberFactory()
        self.account = CurrentAccountFactory(user=self.user)

        self.income_transaction_secu = IncomeTransactionFactory(account=self.account, amount=Decimal("25.00"))

        self.income_transaction_mutuelle = IncomeTransactionFactory(account=self.account, amount=Decimal("20.00"))

        self.expense_transaction = ExpenseTransactionFactory(account=self.account, amount=Decimal("100.00"))

        self.secu = Secu.objects.create(
            theoritical_date=timezone.now(),
            amount=Decimal("30.00"),
            withheld_amount=Decimal("5.00"),
            income_transaction=self.income_transaction_secu,
        )

        self.mutuelle = Mutuelle.objects.create(
            theorical_date=timezone.now(),
            amount=Decimal("20.00"),
            income_transaction=self.income_transaction_mutuelle,
        )

    def test_health_model_creation(self):
        health = Health.objects.create(
            user=self.user,
            amount=Decimal("100.00"),
            subject="Test Health Expense",
            description="Test description",
            expense_transaction=self.expense_transaction,
            secu=self.secu,
            mutuelle=self.mutuelle,
        )

        self.assertEqual(str(health), f"{self.user.trigram} - Test Health Expense - {health.date}")

    def test_reimbursement_total(self):
        health = Health(
            user=self.user,
            amount=Decimal("100.00"),
            subject="Test Health Expense",
            expense_transaction=self.expense_transaction,
            secu=self.secu,
            mutuelle=self.mutuelle,
        )

        self.assertEqual(health.reimbursement_total, Decimal("45.00"))

    def test_remains_amount(self):
        health = Health(
            user=self.user,
            amount=Decimal("100.00"),
            subject="Test Health Expense",
            expense_transaction=self.expense_transaction,
            secu=self.secu,
            mutuelle=self.mutuelle,
        )

        self.assertEqual(health.remains_amount, Decimal("55.00"))

    def test_clean_method_valid(self):
        health = Health(
            user=self.user,
            amount=Decimal("100.00"),
            subject="Test Health Expense",
            expense_transaction=self.expense_transaction,
            secu=self.secu,
            mutuelle=self.mutuelle,
        )
        health.clean()  # Should not raise ValidationError

    def test_clean_method_invalid(self):
        with self.assertRaises(ValidationError):
            health = Health(
                user=self.user,
                amount=Decimal("40.00"),  # Less than reimbursements
                subject="Test Health Expense",
                expense_transaction=self.expense_transaction,
                secu=self.secu,
                mutuelle=self.mutuelle,
            )
            health.clean()

    def test_total_expenses_by_user(self):

        Health.objects.create(
            user=self.user,
            amount=Decimal("100.00"),
            date=timezone.now(),
            subject="Expense 1",
            expense_transaction=self.expense_transaction,
            secu=self.secu,
            mutuelle=self.mutuelle,
        )

        expense_transaction2 = ExpenseTransactionFactory(account=self.account, amount=Decimal("100.00"))

        secu2 = Secu.objects.create(
            theoritical_date=timezone.now(),
            amount=Decimal("30.00"),
            withheld_amount=Decimal("5.00"),
            income_transaction=self.income_transaction_secu,
        )

        mutuelle2 = Mutuelle.objects.create(
            theorical_date=timezone.now(),
            amount=Decimal("20.00"),
            income_transaction=self.income_transaction_mutuelle,
        )

        Health.objects.create(
            user=self.user,
            amount=Decimal("50.00"),
            date=timezone.now(),
            subject="Expense 2",
            expense_transaction=expense_transaction2,
            secu=secu2,
            mutuelle=mutuelle2,
        )

        total_expenses = Health.objects.total_expenses_by_user(self.user)
        self.assertEqual(total_expenses, Decimal("150.00"))
