from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "secretbox.users"

    def ready(self):
        # Importer les signaux
        from . import signals
