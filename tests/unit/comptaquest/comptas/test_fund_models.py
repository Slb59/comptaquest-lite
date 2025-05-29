from django.test import TestCase

from comptaquest.comptas.models.fund import FundDistribution, FundHistory
from tests.factories.account import InvestmentAccountFactory


class TestFundModel(TestCase):
    def setUp(self):
        self.account = InvestmentAccountFactory()
        self.fund_distribution = FundDistribution(
            fund_name="Test Fund",
            prct=50,
            fund_type="Test Type",
            investment_account=self.account,
        )
        self.fun_history = FundHistory(
            date_value="2023-01-01",
            amount=100,
            notes="Test",
            investment_account=self.account,
        )

    def test_fund_creation(self):

        self.assertEqual(self.account.account_type, "Investment")
        self.assertEqual(self.fund_distribution.investment_account, self.account)
        self.assertEqual(self.fund_distribution.fund_name, "Test Fund")
        self.assertEqual(self.fund_distribution.prct, 50)
        self.assertEqual(self.fund_distribution.fund_type, "Test Type")
        self.assertEqual(self.fun_history.investment_account, self.account)
        self.assertEqual(self.fun_history.date_value, "2023-01-01")
        self.assertEqual(self.fun_history.amount, 100)
        self.assertEqual(self.fun_history.notes, "Test")
