import uuid

from django.db import models
from django_countries.fields import CountryField


class NomadePosition(models.Model):
    # Core Information
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    # Location Details
    address = models.TextField()
    city = models.TextField()
    country = CountryField()

    # Rating System
    stars = models.IntegerField(default=0)
    reviews = models.JSONField(default=list)

    # Dates
    opening_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)

    # Category and Position
    category = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

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
