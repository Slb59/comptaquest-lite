import os

import pytest
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }


@pytest.fixture(scope="session", autouse=True)
def django_settings():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
