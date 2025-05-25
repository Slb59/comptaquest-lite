from decimal import Decimal

from django.test import TestCase
from django.utils.timezone import now

from comptaquest.comptas.models.transaction import TransferTransaction
from tests.factories.account import CurrentAccountFactory
from tests.factories.codification import CategoryCodificationFactory


class TestTransferTransactionModel(TestCase):
    def setUp(self):
        self.account1 = CurrentAccountFactory()
        self.account2 = CurrentAccountFactory()
        self.transfer = TransferTransaction(
            date_transaction=now(),
            amount=100,
            account=self.account1,
            link_account=self.account2,
            category=CategoryCodificationFactory(),
        )

    def test_transfer_transaction_creation(self):
        self.assertEqual(self.transfer.amount, 100)
        self.assertEqual(self.transfer.link_account, self.account2)
        self.assertEqual(self.transfer.account, self.account1)
        self.assertEqual(self.transfer.link_transfer, None)

    def test_transfer_transaction_name(self):
        self.assertEqual(
            self.transfer.__str__(),
            f"Transfer {self.transfer.date_transaction}-{self.transfer.amount}: {self.account1}->{self.account2}",
        )

    def test_transfer_transaction_creates_linked_transaction(self):
        # Refresh the transfer from database to get the link
        self.transfer.save()
        self.transfer.refresh_from_db(fields=["link_transfer"])

        # Verify linked transaction exists
        self.assertIsNotNone(self.transfer.link_transfer)

        # Check reverse transaction details
        reverse_transfer = self.transfer.link_transfer
        self.assertEqual(reverse_transfer.amount, Decimal("-100.00"))
        self.assertEqual(reverse_transfer.account, self.account2)
        self.assertEqual(reverse_transfer.link_account, self.account1)

        # Verify bidirectional linking
        self.assertEqual(reverse_transfer.link_transfer, self.transfer)
