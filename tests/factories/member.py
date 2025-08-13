import factory
import pytest
from django.contrib.auth import get_user_model

Member = get_user_model()


@pytest.mark.django_db
class MemberFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Member instances.
    """

    class Meta:
        model = Member

    email = factory.Faker("email")
    trigram = factory.Faker("bothify", text="MB#")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_active = True
    is_staff = False
    is_superuser = False
