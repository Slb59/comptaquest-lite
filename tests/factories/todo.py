from datetime import timedelta

import factory
import factory.fuzzy
import pytest
from django.utils import timezone

from secretbox.dashboard.models import Todo
from secretbox.tools.models import get_now_date, get_random_date_in_current_month

from .member import MemberFactory


@pytest.mark.django_db
class TodoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Todo

    user = factory.SubFactory(MemberFactory)
    state = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.STATE_CHOICES])
    duration = factory.fuzzy.FuzzyInteger(low=10, high=800)
    description = factory.Faker("sentence")
    appointment = factory.LazyFunction(get_random_date_in_current_month)
    category = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.CATEGORY_CHOICES])
    who = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.WHO_CHOICES])
    place = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.PLACE_CHOICES])
    periodic = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.PERIODIC_CHOICES])
    last_execute_date = factory.LazyFunction(get_now_date)
    planned_date = factory.LazyAttribute(lambda obj: get_now_date() + timedelta(days=1))
    priority = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.PRIORITY_CHOICES])

    done_date = factory.LazyAttribute(
        lambda obj: get_now_date() if factory.fuzzy.FuzzyChoice([True, False]) else None
    )
    note = factory.Faker("text")
