import factory
import pytest

from comptaquest.comptas.models.account import (CurrentAccount,
                                                InvestmentAccount)
from tests.factories.member import MemberFactory


@pytest.mark.django_db
class CurrentAccountFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating CurrentAccount instances.
    """

    class Meta:
        model = CurrentAccount

    user = factory.SubFactory(MemberFactory, trigram="MB1")  # defer user creation
    name = factory.Faker("word")
    current_balance = factory.Faker("random_int", min=0, max=1000)
    created_by = factory.SubFactory(MemberFactory)


@pytest.mark.django_db
class InvestmentAccountFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating InvestmentAccount instances.
    """

    class Meta:
        model = InvestmentAccount

    user = factory.SubFactory(MemberFactory, trigram="MB1")  # defer user creation
    name = factory.Faker("word")
    current_balance = factory.Faker("random_int", min=0, max=1000)  # investment balance
    created_by = factory.SubFactory(MemberFactory)
