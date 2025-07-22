from datetime import timedelta

import factory
import factory.fuzzy
import pytest

from secretbox.dashboard.choices import (CATEGORY_CHOICES, PERIODIC_CHOICES,
                                         PLACE_CHOICES, PRIORITY_CHOICES)
from secretbox.dashboard.models import Todo
from secretbox.tools.models import get_now_date


from .member import MemberFactory


@pytest.mark.django_db
class TodoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Todo

    user = factory.SubFactory(MemberFactory)
    state = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.STATE_CHOICES])
    duration = factory.fuzzy.FuzzyInteger(low=10, high=800)
    description = factory.Faker("sentence")
    appointment = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.APPOINTEMENT_CHOICES])
    category = factory.fuzzy.FuzzyChoice([choice[0] for choice in CATEGORY_CHOICES])
    who = factory.SubFactory(MemberFactory)
    place = factory.fuzzy.FuzzyChoice([choice[0] for choice in PLACE_CHOICES])
    periodic = factory.fuzzy.FuzzyChoice([choice[0] for choice in PERIODIC_CHOICES])
    report_date = factory.LazyFunction(get_now_date)
    planned_date = factory.LazyAttribute(lambda obj: get_now_date() + timedelta(days=1))
    priority = factory.fuzzy.FuzzyChoice([choice[0] for choice in PRIORITY_CHOICES])

    done_date = factory.LazyAttribute(lambda obj: get_now_date() if factory.fuzzy.FuzzyChoice([True, False]) else None)
    note = factory.Faker("text")
