import factory
from django_countries import countries

from escapevault.models import NomadePosition


class NomadePositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NomadePosition

    name = factory.Faker("company")
    address = factory.Faker("street_address")
    city = factory.Faker("city")
    country = factory.LazyFunction(lambda: countries.by_name("France"))
    stars = factory.Faker("random_int", min=0, max=5)
    reviews = factory.Faker("text", max_nb_chars=200)
    opening_date = factory.Faker("date", pattern="%d/%m")
    closing_date = factory.Faker("date", pattern="%d/%m")
    category = factory.Faker("word")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")

    # @factory.lazy_attribute
    # def opening_date(self):
    #     return f"{factory.Faker('day_of_month').generate({})}/{factory.Faker('month').generate({})}"

    # @factory.lazy_attribute
    # def closing_date(self):
    #     return f"{factory.Faker('day_of_month').generate({})}/{factory.Faker('month').generate({})}"
