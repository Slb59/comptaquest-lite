import factory
from tests.factories.member import MemberFactory

from comptaquest.utils.models import CategoryCodification, Codification, IncomeCodification, PaymentCodification


class CodificationFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Codification objects.
    """

    class Meta:
        model = Codification

    user = factory.SubFactory(MemberFactory, trigram="MB1")  # defer user creation
    name = factory.Faker("word")
    description = factory.Faker("sentence", nb_words=6)
    state = factory.Iterator(Codification.CodeStatus.values)
    codetype = factory.Iterator(Codification.CodeType.values)


class PaymentCodificationFactory(CodificationFactory):
    """
    Factory for creating PaymentCodification objects.
    """

    class Meta:
        model = PaymentCodification

    codetype = Codification.CodeType.PAYMENT


class IncomeCodificationFactory(CodificationFactory):
    """
    Factory for creating IncomeCodification objects.
    """

    class Meta:
        model = IncomeCodification

    codetype = Codification.CodeType.INCOME


class CategoryCodificationFactory(CodificationFactory):
    """
    Factory for creating CategoryCodification objects.
    """

    class Meta:
        model = CategoryCodification

    codetype = Codification.CodeType.CATEGORY
