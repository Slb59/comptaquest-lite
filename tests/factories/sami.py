import factory
from django.utils import timezone
from your_app.models import Sami  # Replace 'your_app' with the actual app name


class SamiFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sami

    date = factory.LazyFunction(lambda: timezone.now().date())
    weight = factory.Faker("random_int", min=0, max=100)
    bedtime = factory.Faker("random_int", min=0, max=3)
    wakeup = factory.Faker("random_int", min=0, max=3)
    nonstop = factory.Faker("random_int", min=0, max=5)
    energy = factory.Faker("random_int", min=0, max=5)
    naptime = factory.Faker("random_int", min=0, max=4)
    phone = factory.Faker("random_int", min=0, max=2)
    reading = factory.Faker("random_int", min=0, max=3)
    user = factory.SubFactory("your_app.factories.UserFactory")  # Replace with your User factory if needed
