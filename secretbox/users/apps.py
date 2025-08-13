"""Configuration for the secretbox.users application."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """App configuration for secretbox.users."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "secretbox.users"

    def ready(self):
        # Importer les signaux
        from . import signals  # noqa: F401
