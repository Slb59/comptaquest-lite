import factory
import pytest
from factory.django import DjangoModelFactory

from secretbox.dashboard.colorparameter_model import ColorParameter
from secretbox.dashboard.todo_model import (
    CATEGORY_CHOICES,
    PERIODIC_CHOICES,
    PLACE_CHOICES,
    PRIORITY_CHOICES,
)


@pytest.mark.django_db
class ColorParameterFactory(DjangoModelFactory):
    class Meta:
        model = ColorParameter
        django_get_or_create = ("priority", "periodic", "category", "place")

    priority = factory.Iterator([choice[0] for choice in PRIORITY_CHOICES])
    periodic = factory.Iterator([choice[0] for choice in PERIODIC_CHOICES])
    category = factory.Iterator([choice[0] for choice in CATEGORY_CHOICES])
    place = factory.Iterator([choice[0] for choice in PLACE_CHOICES])
    color = factory.Faker("hex_color")  # example : "#A1B2C3"
