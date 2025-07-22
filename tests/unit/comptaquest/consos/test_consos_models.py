from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from comptaquest.consos.models import ConsoEdf, ConsoWater, QualityWater
from tests.factories.place import PlaceFactory


class TestModelValidation(TestCase):
    def setUp(self):
        self.place = PlaceFactory(name="Test Place", city="Test City")

    def test_place_str_method(self):
        self.assertEqual(str(self.place), "Test Place - Test City")

    def test_conso_water_yearly_quantity(self):
        water_conso = ConsoWater.objects.create(place=self.place, quantity=100, date=timezone.now())

        yearly_quantity = water_conso.yearly_quantity()
        self.assertIsInstance(yearly_quantity, int)

    def test_conso_edf_conso_property(self):
        edf_conso = ConsoEdf.objects.create(place=self.place, conso_hc=50, conso_hp=30)

        self.assertEqual(edf_conso.conso, 80)

    def test_quality_water_field_validation(self):
        # Test valid values
        valid_water_quality = QualityWater(
            place=self.place,
            Fluor=1.5,
            hardness=25.5,
            nitrates=25.0,
            pesticides=0.5,
            perchlorates=2.0,
        )
        valid_water_quality.full_clean()

        # Test invalid values
        with self.assertRaises(ValidationError):
            invalid_water_quality = QualityWater(
                place=self.place,
                Fluor=3.0,  # Exceeds max value
                hardness=60.0,  # Exceeds max value
                nitrates=60.0,  # Exceeds max value
                pesticides=2.0,  # Exceeds max value
                perchlorates=4.0,  # Exceeds max value
            )
            invalid_water_quality.full_clean()

    def test_yearly_aggregation(self):
        current_year = timezone.now().year

        # Test Water Consumption Yearly Total
        ConsoWater.objects.create(place=self.place, quantity=100, date=timezone.now(), amount=50.00)
        water_yearly_total = ConsoWater.objects.yearly_total(current_year)
        self.assertEqual(water_yearly_total, Decimal("50.00"))

        # Test Electricity Consumption Yearly Total
        ConsoEdf.objects.create(
            place=self.place,
            conso_hc=50,
            conso_hp=30,
            date=timezone.now(),
            amount=75.00,
        )
        edf_yearly_total = ConsoEdf.objects.yearly_total(current_year)
        self.assertEqual(edf_yearly_total, Decimal("75.00"))
