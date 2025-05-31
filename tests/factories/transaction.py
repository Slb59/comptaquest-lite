import factory

from comptaquest.comptas.models.transaction import (ExpenseTransaction,
                                                    IncomeTransaction,
                                                    TransferTransaction)
from tests.factories.account import CurrentAccountFactory
from tests.factories.codification import (CategoryCodificationFactory,
                                          IncomeCodificationFactory,
                                          PaymentCodificationFactory)


class ExpenseTransactionFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating ExpenseTransaction instances.
    """

    class Meta:
        model = ExpenseTransaction

    account = factory.SubFactory(CurrentAccountFactory)
    amount = factory.Faker("random_int", min=0, max=1000)
    date_transaction = factory.Faker("date_between", start_date="-1y", end_date="today")
    description = factory.Faker("sentence", nb_words=3)
    category = factory.SubFactory(CategoryCodificationFactory)
    payment_method = factory.SubFactory(PaymentCodificationFactory)


class IncomeTransactionFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating IncomeTransaction Instances.
    """

    class Meta:
        model = IncomeTransaction

    account = factory.SubFactory(CurrentAccountFactory)
    amount = factory.Faker("random_int", min=0, max=1000)
    date_transaction = factory.Faker("date_between", start_date="-1y", end_date="today")
    description = factory.Faker("sentence", nb_words=3)
    category = factory.SubFactory(CategoryCodificationFactory)
    income_method = factory.SubFactory(IncomeCodificationFactory)


class TransferTransactionFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating TransferTransaction Instances.
    """

    class Meta:
        model = TransferTransaction

    account = factory.SubFactory(CurrentAccountFactory)
    amount = factory.Faker("random_int", min=0, max=1000)
    date_transaction = factory.Faker("date_between", start_date="-1y", end_date="today")
    description = factory.Faker("sentence", nb_words=3)
    category = factory.SubFactory(CategoryCodificationFactory)
    link_account = factory.SubFactory(CurrentAccountFactory)
