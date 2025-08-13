from .base import *  # noqa: F403 F401

DEBUG = True
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db_test.sqlite3"),  # noqa: F405
        "ATOMIC_REQUESTS": True,
    }
}
