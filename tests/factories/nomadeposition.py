import secrets
from datetime import datetime

import factory
import factory.fuzzy
import pytest
from django_countries import countries
from faker import Faker

from escapevault.models import NomadePosition

fake = Faker()


@pytest.mark.django_db
class NomadePositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NomadePosition

    name = factory.Faker("company")
    address = factory.Faker("street_address")
    city = factory.Faker("city")
    country = factory.LazyFunction(lambda: countries.by_name("France"))
    stars = factory.Faker("random_int", min=1, max=5)

    opening_date = factory.Faker("date", pattern="%d/%m")
    closing_date = factory.Faker("date", pattern="%d/%m")
    category = factory.fuzzy.FuzzyChoice(
        [choice[0] for choice in NomadePosition.CATEGORY_CHOICES]
    )
    latitude = factory.fuzzy.FuzzyDecimal(low=-90.0, high=90.0)
    longitude = factory.fuzzy.FuzzyDecimal(low=-90.0, high=90.0)

    @factory.lazy_attribute
    def reviews(self):
        return [
            {"text": fake.text(max_nb_chars=200), "date": datetime.now().isoformat()}
            for _ in range(secrets.randbelow(3) + 1)
        ]
