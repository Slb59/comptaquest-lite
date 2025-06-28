import os

import pytest
from django.conf import settings


@pytest.fixture(scope="session", autouse=True)
def django_test_config():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": True,
    }