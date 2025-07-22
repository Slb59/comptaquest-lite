import factory
import pytest
from factory.django import DjangoModelFactory

from comptaquest.consos.models import Place


@pytest.mark.django_db
class PlaceFactory(DjangoModelFactory):
    class Meta:
        model = Place

    name = factory.Faker("company")
    address = factory.Faker("street_address")
    city = factory.Faker("city")
