import factory
import pytest
from faker import Faker

from diarylab.models import DiaryEntry
from tests.factories.member import MemberFactory

fake = Faker()


@pytest.mark.django_db
class DiaryEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DiaryEntry

    date = factory.LazyAttribute(lambda _: fake.date_time().date())
    content = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=500))
    user = factory.SubFactory(MemberFactory)
