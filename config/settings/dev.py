from .base import *  # noqa F403

# from .base import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = ["*"]

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
NPM_BIN_PATH = env("NPM_BIN_PATH")