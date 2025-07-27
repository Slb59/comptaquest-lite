"""Lists of values used as choices in Django template fields.

This file centralizes type constants (value, label)
to ensure consistency between models, forms and display.
"""

ACCOUNT_CHOICES = [("Current", "Compte courant"), ("Investment", "Compte d'investissement")]

BANK_CHOICES = [
    ("CE", "CE"),
    ("CA", "CA"),
    ("GMF", "GMF"),
]
