import factory
import pytest

from sami.models import Sami
from secretbox.tools.date_tools import get_now_date
from tests.factories.member import MemberFactory


@pytest.mark.django_db
class SamiFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sami

    user = factory.SubFactory(MemberFactory)
    date = factory.LazyFunction(get_now_date)
    weight = factory.Faker("pyint", min_value=0, max_value=100)
    bedtime = factory.Faker("pyint", min_value=0, max_value=3)
    wakeup = factory.Faker("pyint", min_value=0, max_value=3)
    nonstop = factory.Faker("pyint", min_value=0, max_value=5)
    energy = factory.Faker("pyint", min_value=0, max_value=5)
    naptime = factory.Faker("pyint", min_value=0, max_value=4)
    phone = factory.Faker("pyint", min_value=0, max_value=2)
    reading = factory.Faker("pyint", min_value=0, max_value=3)

    fruits = factory.Faker("pyint", min_value=0, max_value=3)
    vegetables = factory.Faker("pyint", min_value=0, max_value=2)
    meals = factory.Faker("pyint", min_value=0, max_value=5)
    desserts = factory.Faker("pyint", min_value=0, max_value=5)
    sugardrinks = factory.Faker("pyint", min_value=0, max_value=5)
    nosugardrinks = factory.Faker("pyint", min_value=0, max_value=5)

    homework = factory.Faker("pyint", min_value=0, max_value=5)
    garden = factory.Faker("pyint", min_value=0, max_value=5)
    Outsidetime = factory.Faker("pyint", min_value=0, max_value=5)
    endurancesport = factory.Faker("pyint", min_value=0, max_value=5)
    yogasport = factory.Faker("pyint", min_value=0, max_value=5)

    videogames = factory.Faker("pyint", min_value=0, max_value=5)
    papergames = factory.Faker("pyint", min_value=0, max_value=5)
    administrative = factory.Faker("pyint", min_value=0, max_value=5)
    computer = factory.Faker("pyint", min_value=0, max_value=5)
    youtube = factory.Faker("pyint", min_value=0, max_value=5)
