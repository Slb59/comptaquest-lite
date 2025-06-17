import re
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


def validate_day_month_format(value):
    # Utilisez une expression régulière pour valider le format DD/MM
    if not re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])$", value):
        raise ValidationError("The correct format is DD/MM.")


class NomadePosition(models.Model):
    # Core Information
    name = models.CharField(max_length=255)

    # Location Details
    address = models.TextField()
    city = models.TextField()
    country = CountryField(blank_label=_("France"))

    # Rating System
    stars = models.IntegerField(default=0)
    reviews = models.JSONField(default=list)
    # Dates
    opening_date = models.CharField(max_length=5, validators=[validate_day_month_format], null=True, blank=True)
    closing_date = models.CharField(max_length=5, validators=[validate_day_month_format], null=True, blank=True)

    # Category and Position
    category = models.CharField(max_length=100)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )

    def get_position(self):
        return (self.latitude, self.longitude)

    def set_position(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        verbose_name = "Nomade Position"
        verbose_name_plural = "Nomade Positions"
