import factory
from factory.django import DjangoModelFactory
from secretbox.dashboard.models import (
    CATEGORY_CHOICES, PERIODIC_CHOICES, PLACE_CHOICES, PRIORITY_CHOICES,
    ColorParameter)

@pytest.mark.django_db
class ColorParameterFactory(DjangoModelFactory):
    class Meta:
        model = ColorParameter

    priority = factory.Iterator([choice[0] for choice in PRIORITY_CHOICES])
    periodicity = factory.Iterator([choice[0] for choice in PERIODIC_CHOICES])
    category = factory.Iterator([choice[0] for choice in CATEGORY_CHOICES])
    place = factory.Iterator([choice[0] for choice in PLACE_CHOICES])
    color = factory.Faker("hex_color")  # exemple : "#A1B2C3"
