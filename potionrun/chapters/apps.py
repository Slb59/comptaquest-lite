"""Configuration for the potionrun.chapters application."""

from django.apps import AppConfig


class ChaptersConfig(AppConfig):
    """App configuration for potionrun.chapters."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "potionrun.chapters"

    def ready(self):
        # Importer les signaux
        from . import signals  # noqa: F401
