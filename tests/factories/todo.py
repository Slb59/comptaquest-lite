from datetime import timedelta

import factory
import factory.fuzzy
from django.utils import timezone

from secretbox.dashboard.models import Todo

from .member import MemberFactory


class TodoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Todo

    user = MemberFactory()
    state = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.STATE_CHOICES])
    duration = factory.fuzzy.FuzzyNaiveTimeDelta(start_dt=timedelta(hours=1), end_dt=timedelta(days=1))
    description = factory.Faker("sentence")
    appointment = factory.fuzzy.FuzzyDateTime(start_dt=timezone.now(), end_dt=timezone.now() + timedelta(days=30))
    category = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.CATEGORY_CHOICES])
    who = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.WHO_CHOICES])
    place = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.PLACE_CHOICES])
    periodic = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.PERIODIC_CHOICES])
    current_date = factory.LazyFunction(lambda: timezone.now().date())
    planned_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=1))
    priority = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.PRIORITY_CHOICES])
    done = factory.Maybe(
        "is_done", yes_declaration=factory.LazyFunction(lambda: timezone.now().date()), no_declaration=None
    )
    note = factory.Faker("text")

    @factory.lazy_attribute
    def is_done(self):
        return factory.Faker("boolean").generate({})
