"""Lists of values used as choices in Django template fields.

This file centralizes type constants (value, label)
to ensure consistency between models, forms and display.
"""

from django.utils.translation import gettext_lazy as _

ACCOUNT_CHOICES = [("Current", _("Compte bancaire")), ("Investment", _("Compte d'investissement"))]

BANK_CHOICES = [
    ("CE", "CE"),
    ("CA", "CA"),
    ("GMF", "GMF"),
]

STATE_CHOICES = [("Open", _("Ouvert")), ("Close", _("Fermé"))]
