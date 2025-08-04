from datetime import timedelta

import factory
import factory.fuzzy
import pytest

from secretbox.dashboard.choices import (
    CATEGORY_CHOICES,
    PERIODIC_CHOICES,
    PLACE_CHOICES,
    PRIORITY_CHOICES,
)
from secretbox.dashboard.todo_model import Todo
from secretbox.tools.date_tools import get_now_date

from .member import MemberFactory


@pytest.mark.django_db
class TodoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Todo

    user = factory.SubFactory(MemberFactory)
    state = factory.fuzzy.FuzzyChoice([choice[0] for choice in Todo.STATE_CHOICES])
    duration = factory.fuzzy.FuzzyInteger(low=10, high=800)
    description = factory.Faker("sentence")
    appointment = factory.fuzzy.FuzzyChoice(
        [choice[0] for choice in Todo.APPOINTEMENT_CHOICES]
    )
    category = factory.fuzzy.FuzzyChoice([choice[0] for choice in CATEGORY_CHOICES])
    place = factory.fuzzy.FuzzyChoice([choice[0] for choice in PLACE_CHOICES])
    periodic = factory.fuzzy.FuzzyChoice([choice[0] for choice in PERIODIC_CHOICES])
    report_date = factory.LazyFunction(get_now_date)
    planned_date = factory.LazyAttribute(lambda obj: get_now_date() + timedelta(days=1))
    priority = factory.fuzzy.FuzzyChoice([choice[0] for choice in PRIORITY_CHOICES])

    done_date = factory.LazyAttribute(
        lambda obj: get_now_date() if factory.fuzzy.FuzzyChoice([True, False]) else None
    )
    note = factory.Faker("text")

    @factory.post_generation
    def who(self, create, extracted, **kwargs):
        """
        manage ManyToMany relation after object creation.
        `extracted` could be a list of users or a single user.
        """
        if not create:
            # Si on fait build() au lieu de create(), on ne touche pas aux relations M2M
            return

        if extracted:
            for user in extracted:
                self.who.add(user)
        else:
            # Par défaut : ajouter un seul membre factice
            user = MemberFactory()
            self.who.add(user)
