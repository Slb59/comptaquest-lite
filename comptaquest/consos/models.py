from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class Place(models.Model):
    """
    Represents a physical location with basic identifying information.

    Attributes:
        name (CharField): Name of the place.
        address (CharField): Street address of the place.
        city (CharField): City where the place is located.
    """

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.city}"


class YearlyAggregationManager(models.Manager):
    def yearly_total(self, year=None):
        """
        Calculate yearly total for a specific field.

        Args:
            year (int, optional): Year to calculate total. Defaults to current year.

        Returns:
            Decimal or int: Total for the specified year
        """
        if year is None:
            year = timezone.now().year

        return self.filter(date__year=year).aggregate(total=Sum("amount"))["total"] or 0


class Conso(models.Model):
    """
    Abstract base model for consumption tracking.

    Attributes:
        date (DateField): Date of consumption record, automatically set when created.
        amount (DecimalField): Monetary or quantitative amount of consumption.
        description (CharField): Description of the consumption.
        place (ForeignKey): Related Place where consumption occurred.
    """

    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(default=0, max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=255, blank=True, null=True)
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="%(class)s_place_consos",
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(TypedModelMeta):
        """Meta options for Conso model."""

        verbose_name = "Conso"
        verbose_name_plural = "Consos"
        abstract = True
        ordering = ["-date"]


class QualityWater(Conso):
    """
    Model to track water quality measurements.

    Attributes:
        Microbiology (DecimalField): Microbiological measurement.
        Fluor (DecimalField): Fluoride content.
        hardness (DecimalField): Water hardness measurement.
        nitrates (DecimalField): Nitrate levels.
        pesticides (DecimalField): Pesticide content.
        perchlorates (DecimalField): Perchlorate levels.
    """

    Microbiology = models.DecimalField(
        default=0,
        help_text=_("Microbiological measurement."),
        max_digits=5,
        decimal_places=1,
    )
    Fluor = models.DecimalField(
        default=0,
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        help_text=_("mg/l"),
    )
    hardness = models.DecimalField(
        default=0,
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        help_text=_("°f"),
    )
    nitrates = models.DecimalField(
        default=0,
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        help_text=_("mg/l"),
    )
    pesticides = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_("ug/l"),
    )
    perchlorates = models.DecimalField(
        default=0,
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text=_("ug/l"),
    )


class ConsoWater(Conso):
    """
    Model to track water consumption.

    Attributes:
        quantity (IntegerField): Volume of water consumed.
    Use for total call:
        water_yearly_amount = ConsoWater.objects.yearly_total(2024)
        water_yearly_quantity = ConsoWater.objects.first().yearly_quantity(2024)
    """

    objects = YearlyAggregationManager()
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def yearly_quantity(self, year=None):
        """
        Calculate total water quantity for a year.

        Args:
            year (int, optional): Year to calculate total. Defaults to current year.

        Returns:
            int: Total water quantity for the year
        """
        if year is None:
            year = timezone.now().year

        return (
            self.__class__.objects.filter(date__year=year).aggregate(total_quantity=Sum("quantity"))["total_quantity"]
            or 0
        )


class ConsoEdf(Conso):
    """
    Model to track electricity consumption.

    Attributes:
        conso_hc (IntegerField): Low-hour electricity consumption.
        conso_hp (IntegerField): Peak-hour electricity consumption.

    Properties:
        conso (int): Total electricity consumption (sum of low and peak hours).
    Use for total call:
        edf_yearly_amount = ConsoEdf.objects.yearly_total(2024)
        edf_yearly_conso = ConsoEdf.objects.first().yearly_total_conso(2024)
    """

    objects = YearlyAggregationManager()
    conso_hc = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    conso_hp = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    @property
    def conso(self):
        """
        Calculate total electricity consumption.

        Returns:
            int: Sum of low-hour and peak-hour consumption.
        """
        return self.conso_hc + self.conso_hp

    def yearly_total_conso(self, year=None):
        """
        Calculate total electricity consumption for a year.

        Args:
            year (int, optional): Year to calculate total. Defaults to current year.

        Returns:
            int: Total electricity consumption for the year
        """
        if year is None:
            year = timezone.now().year

        yearly_data = self.__class__.objects.filter(date__year=year).aggregate(
            total_hc=Sum("conso_hc"), total_hp=Sum("conso_hp")
        )

        return (yearly_data["total_hc"] or 0) + (yearly_data["total_hp"] or 0)
