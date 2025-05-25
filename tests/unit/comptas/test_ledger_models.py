from django.core.exceptions import ValidationError
from django.test import TestCase

from comptaquest.comptas.models.ledger import Ledger
from tests.factories.member import MemberFactory


class TestLedgerModel(TestCase):

    def setUp(self):
        self.user = MemberFactory()
        self.ledger = Ledger(user=self.user)

    def test_ledger_creation(self):
        self.assertEqual(self.ledger.user, self.user)
        self.assertEqual(self.ledger.start_date, None)
        self.assertEqual(self.ledger.end_date, None)
        self.assertEqual(self.ledger.status, "Open")

    def test_ledger_clean(self):
        self.ledger.start_date = "2023-01-01"
        self.ledger.end_date = "2023-01-01"
        self.ledger.status = "Open"
        self.ledger.full_clean()

    def test_ledger_invalid_clean(self):
        self.ledger.start_date = "2023-01-02"
        self.ledger.end_date = "2023-01-01"
        self.ledger.status = "Open"
        with self.assertRaises(ValidationError):
            self.ledger.full_clean()
