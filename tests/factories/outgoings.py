import factory
import pytest

from comptaquest.comptas.models.outgoings import ExpenseOutgoings
from tests.factories.account import CurrentAccountFactory
from tests.factories.codification import (
    CategoryCodificationFactory,
    PaymentCodificationFactory,
)
from tests.factories.member import MemberFactory


@pytest.mark.django_db
class ExpenseOutgoingsFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating ExpenseOutgoings instances.
    """

    class Meta:
        model = ExpenseOutgoings

    account = factory.SubFactory(CurrentAccountFactory)
    name = factory.Faker("sentence", nb_words=3)
    category = factory.SubFactory(CategoryCodificationFactory)
    payment_method = factory.SubFactory(PaymentCodificationFactory)
    last_integrated_date = factory.Faker(
        "date_between", start_date="-1y", end_date="today"
    )
    periodicity = "Monthly"
    start_date = factory.Faker("date_between", start_date="-1y", end_date="today")
    end_date = factory.Faker("date_between", start_date="-1y", end_date="today")
    amount = factory.Faker("random_int", min=0, max=1000)
    description = factory.Faker("sentence", nb_words=3)
    created_by = factory.SubFactory(MemberFactory)
