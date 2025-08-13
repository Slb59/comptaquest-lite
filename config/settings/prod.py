from .base import *  # noqa: F403 F401

DEBUG = False

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# TODO : définir les paramètres de l'envoi de mail
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'user@example.com'
# EMAIL_HOST_PASSWORD = 'password'
