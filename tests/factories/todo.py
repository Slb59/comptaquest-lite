from datetime import timedelta

import factory
import factory.fuzzy
import pytest
from django.utils import timezone

from secretbox.dashboard.models import Todo

from .member import MemberFactory


@pytest.mark.django_db
class TodoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Todo

    user = factory.SubFactory(MemberFactory)
    state = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.STATE_CHOICES])
    duration = factory.fuzzy.FuzzyInteger(low=10, high=800)
    description = factory.Faker("sentence")
    appointment = factory.fuzzy.FuzzyDateTime(start_dt=timezone.now(), end_dt=timezone.now() + timedelta(days=30))
    category = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.CATEGORY_CHOICES])
    who = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.WHO_CHOICES])
    place = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.PLACE_CHOICES])
    periodic = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.PERIODIC_CHOICES])
    current_date = factory.LazyFunction(lambda: timezone.now().date())
    planned_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=1))
    priority = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.PRIORITY_CHOICES])

    done = factory.LazyAttribute(
        lambda obj: timezone.now().date() if factory.fuzzy.FuzzyChoice([True, False]) else None
    )
    note = factory.Faker("text")
