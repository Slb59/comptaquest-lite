from django.apps import AppConfig


class ChaptersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "potionrun.chapters"

    def ready(self):
        # Importer les signaux
        from . import signals
