from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


def bounded_integer_field(
    min_value: int, max_value: int, help_text: str, default=0
):
    return models.IntegerField(
        validators=[MinValueValidator(min_value), MaxValueValidator(max_value)],
        help_text=_(help_text),
        default=default,
    )