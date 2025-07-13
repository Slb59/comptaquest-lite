from decimal import Decimal

from django.db.models import ProtectedError
from django.test import TestCase
from django.utils.timezone import now

from comptaquest.comptas.models.transaction import (ExpenseTransaction,
                                                    TransferTransaction)
from tests.factories.account import CurrentAccountFactory
from tests.factories.transaction import (ExpenseTransactionFactory,
                                         TransferTransactionFactory)


class TestTransactionSoftDelete(TestCase):
    def setUp(self):
        """Set up test data."""
        # Create test accounts
        self.account1 = CurrentAccountFactory()
        self.account2 = CurrentAccountFactory()

        # Create a basic expense transaction
        self.expense = ExpenseTransactionFactory(
            account=self.account1,
            amount=Decimal("100.00"),
        )

        # Create a transfer transaction pair
        self.transfer = TransferTransactionFactory(
            account=self.account1, link_account=self.account2
        )

    def test_expense_soft_delete(self):
        """Test soft delete of a regular expense transaction."""
        # Verify initial status
        self.assertEqual(
            self.expense.status, 
            ExpenseTransaction.TransactionStatus.ACTIVE
        )

        # Perform soft delete
        self.expense.delete()

        # Refresh from database and verify status
        self.expense.refresh_from_db()
        self.assertEqual(
            self.expense.status, 
            ExpenseTransaction.TransactionStatus.DELETED
        )

        # Verify transaction still exists in database
        self.assertTrue(
            ExpenseTransaction.objects.filter(pk=self.expense.pk).exists()
        )

    def test_pointed_expense_protection(self):
        """Test that pointed transactions cannot be deleted."""
        # Mark transaction as pointed
        self.expense.date_pointed = now()
        self.expense.save()

        # Attempt to delete should raise ProtectedError
        with self.assertRaises(ProtectedError):
            self.expense.delete()

        # Verify status remained active
        self.expense.refresh_from_db()
        self.assertEqual(
            self.expense.status, 
            ExpenseTransaction.TransactionStatus.ACTIVE
        )

    def test_transfer_soft_delete(self):
        """Test soft delete of a transfer transaction and its reciprocal."""
        # Get the reciprocal transaction
        reciprocal = self.transfer.link_transfer

        # Verify initial status of both transactions
        self.assertEqual(
            self.transfer.status, 
            TransferTransaction.TransactionStatus.ACTIVE
        )
        self.assertEqual(
            reciprocal.status, 
            TransferTransaction.TransactionStatus.ACTIVE
        )

        # Perform soft delete
        self.transfer.delete()

        # Refresh from database and verify both transactions are marked as deleted
        self.transfer.refresh_from_db()
        reciprocal.refresh_from_db()

        self.assertEqual(
            self.transfer.status, 
            TransferTransaction.TransactionStatus.DELETED
        )
        self.assertEqual(
            reciprocal.status, 
            TransferTransaction.TransactionStatus.DELETED
        )

        # Verify both transactions still exist in database
        self.assertTrue(TransferTransaction.objects.filter(pk=self.transfer.pk).exists())
        self.assertTrue(TransferTransaction.objects.filter(pk=reciprocal.pk).exists())

    def test_pointed_transfer_protection(self):
        """Test that pointed transfer transactions cannot be deleted."""
        # Mark transfer as pointed
        self.transfer.date_pointed = now()
        self.transfer.save()

        # Attempt to delete should raise ProtectedError
        with self.assertRaises(ProtectedError):
            self.transfer.delete()

        # Verify status remained active for both transactions
        self.transfer.refresh_from_db()
        self.transfer.link_transfer.refresh_from_db()

        self.assertEqual(self.transfer.status, TransferTransaction.TransactionStatus.ACTIVE)
        self.assertEqual(
            self.transfer.link_transfer.status,
            TransferTransaction.TransactionStatus.ACTIVE,
        )

    def test_pointed_reciprocal_transfer_protection(self):
        """Test that transfers cannot be deleted if reciprocal is pointed."""
        # Mark reciprocal transfer as pointed
        reciprocal = self.transfer.link_transfer
        reciprocal.date_pointed = now()
        reciprocal.save()

        # Attempt to delete original transfer should raise ProtectedError
        with self.assertRaises(ProtectedError):
            self.transfer.delete()

        # Verify status remained active for both transactions
        self.transfer.refresh_from_db()
        reciprocal.refresh_from_db()

        self.assertEqual(self.transfer.status, TransferTransaction.TransactionStatus.ACTIVE)
        self.assertEqual(reciprocal.status, TransferTransaction.TransactionStatus.ACTIVE)

    def test_active_transactions_query(self):
        """Test querying for active vs deleted transactions."""
        # Create additional test transactions
        expense2 = ExpenseTransactionFactory()
        # Delete one transaction
        self.expense.delete()

        # Test filtering active transactions
        active_expenses = ExpenseTransaction.objects.filter(status=ExpenseTransaction.TransactionStatus.ACTIVE)
        self.assertEqual(active_expenses.count(), 1)
        self.assertEqual(active_expenses.first(), expense2)

        # Test filtering deleted transactions
        deleted_expenses = ExpenseTransaction.objects.filter(status=ExpenseTransaction.TransactionStatus.DELETED)
        self.assertEqual(deleted_expenses.count(), 1)
        self.assertEqual(deleted_expenses.first(), self.expense)

    def test_transfer_delete_integrity(self):
        """Test that deleting one side of a transfer affects both sides."""
        reciprocal = self.transfer.link_transfer

        # Delete from reciprocal side
        reciprocal.delete()

        # Verify both sides are marked as deleted
        self.transfer.refresh_from_db()
        reciprocal.refresh_from_db()

        self.assertEqual(
            self.transfer.status, 
            TransferTransaction.TransactionStatus.DELETED
        )
        self.assertEqual(
            reciprocal.status, 
            TransferTransaction.TransactionStatus.DELETED
        )
